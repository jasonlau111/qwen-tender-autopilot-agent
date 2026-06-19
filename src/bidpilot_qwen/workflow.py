"""Deterministic workflow core for the BidPilot Qwen demo."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

from .models import EvidenceHit, Requirement, ReviewTask, WorkflowResult
from .qwen_client import QwenClient


MANDATORY_TERMS = (
    "must",
    "shall",
    "required",
    "mandatory",
    "non-responsive",
    "disqualification",
    "deadline",
)
REVIEW_SENSITIVE_CATEGORIES = {"legal", "pricing", "delivery", "security", "deadline"}


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _category_for(text: str) -> str:
    lowered = text.lower()
    if "soc 2" in lowered or "security" in lowered:
        return "security"
    if "language" in lowered or "english" in lowered or "chinese" in lowered:
        return "technical"
    if "price" in lowered or "pricing" in lowered or "spreadsheet" in lowered:
        return "pricing"
    if "deadline" in lowered or re.search(r"20\d{2}-\d{2}-\d{2}", lowered):
        return "deadline"
    if "retention" in lowered or "deletion" in lowered or "non-responsive" in lowered:
        return "legal"
    if "support" in lowered or "sla" in lowered or "response" in lowered:
        return "delivery"
    if "public sector" in lowered or "customer" in lowered:
        return "evaluation"
    return "other"


def _owner_for(category: str) -> str:
    return {
        "security": "security",
        "pricing": "finance",
        "deadline": "proposal_manager",
        "legal": "legal",
        "delivery": "technical_lead",
        "technical": "technical_lead",
        "evaluation": "proposal_manager",
    }.get(category, "unassigned")


def _evidence_need_for(text: str, category: str) -> list[str]:
    lowered = text.lower()
    if "soc 2" in lowered:
        return ["SOC 2 Type II report or bridge letter"]
    if "support" in lowered or "sla" in lowered:
        return ["support policy or SLA terms"]
    if "english" in lowered or "chinese" in lowered:
        return ["product localization documentation"]
    if "retention" in lowered or "deletion" in lowered:
        return ["data retention and deletion policy"]
    if category == "pricing":
        return ["completed pricing spreadsheet"]
    if category == "evaluation":
        return ["public sector case study or approved customer reference"]
    return ["approved company evidence"]


def _risk_for(text: str, mandatory: bool) -> str:
    lowered = text.lower()
    if "non-responsive" in lowered or "disqualification" in lowered:
        return "high"
    if mandatory:
        return "medium"
    return "low"


def _due_date_for(text: str) -> str | None:
    match = re.search(r"(20\d{2}-\d{2}-\d{2})", text)
    return match.group(1) if match else None


def extract_requirements(
    rfp_text: str,
    opportunity_id: str,
    source_document: str = "examples/sample-input.md",
) -> list[Requirement]:
    """Extract demo requirements using transparent heuristics."""

    requirements: list[Requirement] = []
    for raw_line in rfp_text.splitlines():
        line = _normalize_text(re.sub(r"^\d+\.\s*", "", raw_line.strip()))
        if not line:
            continue
        lowered = line.lower()
        mandatory = any(term in lowered for term in MANDATORY_TERMS)
        category = _category_for(line)
        requirement_id = f"REQ-{len(requirements) + 1:04d}"
        confidence = 0.9 if mandatory else 0.74
        requirements.append(
            Requirement(
                opportunity_id=opportunity_id,
                requirement_id=requirement_id,
                category=category,
                requirement_text=line,
                normalized_requirement=line.rstrip("."),
                mandatory=mandatory,
                disqualification_risk=_risk_for(line, mandatory),
                source_document=source_document,
                source_section="RFP Text",
                confidence=confidence,
                due_date=_due_date_for(line),
                owner_role=_owner_for(category),
                evidence_needed=_evidence_need_for(line, category),
            )
        )
    return requirements


def parse_evidence_bundle(evidence_text: str) -> list[EvidenceHit]:
    """Parse simple evidence sections from the demo input."""

    pattern = re.compile(
        r"Evidence\s+([A-Z]):\s*(?P<section>[^\n]+)\n(?P<body>.*?)(?=\n\nEvidence\s+[A-Z]:|\Z)",
        re.DOTALL,
    )
    evidence: list[EvidenceHit] = []
    for match in pattern.finditer(evidence_text.strip()):
        evidence.append(
            EvidenceHit(
                evidence_id=f"EVID-{match.group(1)}",
                source_document="Approved Evidence Bundle",
                source_section=_normalize_text(match.group("section")),
                relevance_score=0.0,
                quote_or_summary=_normalize_text(match.group("body")),
            )
        )
    return evidence


def _keyword_score(requirement: Requirement, evidence: EvidenceHit) -> float:
    text = f"{requirement.requirement_text} {' '.join(requirement.evidence_needed)}".lower()
    haystack = f"{evidence.source_section} {evidence.quote_or_summary}".lower()
    keyword_groups = {
        "soc 2": ("soc 2", "security", "type ii"),
        "support": ("support", "sla", "response"),
        "language": ("english", "chinese", "localization"),
        "data": ("retention", "deletion", "data"),
        "pricing": ("pricing", "spreadsheet"),
        "public sector": ("public sector", "customer", "deployment"),
    }
    best = 0.0
    for trigger, terms in keyword_groups.items():
        if trigger in text or any(term in text for term in terms):
            overlap = sum(1 for term in terms if term in haystack)
            best = max(best, min(1.0, overlap / max(2, len(terms))))
    return round(best, 2)


def attach_evidence(requirements: list[Requirement], evidence: list[EvidenceHit]) -> None:
    for requirement in requirements:
        hits: list[EvidenceHit] = []
        for item in evidence:
            score = _keyword_score(requirement, item)
            if score >= 0.5:
                hits.append(
                    EvidenceHit(
                        evidence_id=item.evidence_id,
                        source_document=item.source_document,
                        source_section=item.source_section,
                        relevance_score=score,
                        quote_or_summary=item.quote_or_summary,
                    )
                )
        requirement.available_evidence = sorted(
            hits, key=lambda item: item.relevance_score, reverse=True
        )[:2]


def classify_status(requirement: Requirement, review_threshold: float) -> None:
    needs_sensitive_review = requirement.category in REVIEW_SENSITIVE_CATEGORIES
    if requirement.category == "deadline" and requirement.due_date:
        requirement.status = "needs_review"
        requirement.recommended_action = "Confirm the date and add it to the proposal calendar."
        requirement.review_notes = "Deadline extracted from the RFP and requires human calendar confirmation."
        return
    if requirement.mandatory and not requirement.available_evidence:
        requirement.status = "blocker"
        requirement.recommended_action = "Find approved evidence before drafting a claim."
        requirement.review_notes = "Mandatory requirement has no supporting evidence."
        return
    if requirement.confidence < review_threshold or needs_sensitive_review:
        requirement.status = "needs_review"
        requirement.recommended_action = "Human owner must approve before bid response."
        requirement.review_notes = "Review-sensitive category or confidence threshold triggered."
        return
    if requirement.available_evidence:
        requirement.status = "draft_ready"
        requirement.recommended_action = "Draft response can be reviewed with citations."
        requirement.review_notes = "Evidence found; human approval still recommended."
        return
    requirement.status = "needs_review"
    requirement.recommended_action = "Clarify whether evidence is needed."
    requirement.review_notes = "No evidence matched this optional or evaluation-oriented item."


def create_review_task(requirement: Requirement) -> ReviewTask | None:
    if requirement.status not in {"blocker", "needs_review"}:
        return None
    priority = "high" if requirement.status == "blocker" else "medium"
    reason = requirement.review_notes or "Human checkpoint required."
    return ReviewTask(
        requirement_id=requirement.requirement_id,
        owner_role=requirement.owner_role,
        priority=priority,
        reason=reason,
        required_action=requirement.recommended_action,
    )


def _fallback_draft(requirement: Requirement) -> str:
    if not requirement.available_evidence:
        return (
            f"{requirement.requirement_id}: No draft generated. "
            "Approved evidence is required before making a compliance claim."
        )
    evidence = requirement.available_evidence[0]
    return (
        f"{requirement.requirement_id}: Based on {evidence.source_document}, "
        f"{evidence.source_section}, the response can state: "
        f"{evidence.quote_or_summary} "
        f"[{evidence.source_document}, {evidence.source_section}]"
    )


def draft_response(requirement: Requirement, qwen_client: QwenClient | None) -> str:
    if not requirement.available_evidence:
        return _fallback_draft(requirement)
    if qwen_client and qwen_client.enabled:
        evidence_lines = "\n".join(
            f"- {item.source_document}, {item.source_section}: {item.quote_or_summary}"
            for item in requirement.available_evidence
        )
        response = qwen_client.complete(
            system_prompt=(
                "You draft concise RFP answers from approved evidence only. "
                "Never add facts not present in the evidence. Include citations."
            ),
            user_prompt=(
                f"Requirement: {requirement.requirement_text}\n"
                f"Evidence:\n{evidence_lines}\n\n"
                "Draft a short answer with citations."
            ),
        )
        if response:
            return response
    return _fallback_draft(requirement)


def run_workflow(
    rfp_text: str,
    evidence_text: str,
    opportunity_id: str,
    use_qwen: bool = False,
    review_threshold: float = 0.8,
) -> WorkflowResult:
    agent_trace = [
        "Intake Router Agent accepted opportunity package.",
        "Requirement Extractor Agent parsed RFP obligations.",
    ]
    requirements = extract_requirements(rfp_text, opportunity_id)
    evidence = parse_evidence_bundle(evidence_text)
    attach_evidence(requirements, evidence)
    agent_trace.append("Evidence Scout Agent matched approved evidence.")

    for requirement in requirements:
        classify_status(requirement, review_threshold)

    qwen_client = QwenClient.from_env() if use_qwen else None
    draft_responses = {
        requirement.requirement_id: draft_response(requirement, qwen_client)
        for requirement in requirements
        if requirement.available_evidence
    }
    agent_trace.append("Compliance Reasoner and Draft Writer Agents produced drafts.")

    review_tasks = [
        task
        for task in (create_review_task(requirement) for requirement in requirements)
        if task is not None
    ]
    agent_trace.append("Human Review Gatekeeper created owner-specific tasks.")
    return WorkflowResult(
        opportunity_id=opportunity_id,
        requirements=requirements,
        review_tasks=review_tasks,
        draft_responses=draft_responses,
        agent_trace=agent_trace,
    )


def export_result(result: WorkflowResult, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    requirements_payload = [item.to_dict() for item in result.requirements]
    (output_dir / "requirements.json").write_text(
        json.dumps(requirements_payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    with (output_dir / "compliance_matrix.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "requirement_id",
                "category",
                "mandatory",
                "status",
                "owner_role",
                "disqualification_risk",
                "due_date",
                "evidence_count",
                "requirement_text",
                "recommended_action",
            ],
        )
        writer.writeheader()
        for item in result.requirements:
            writer.writerow(
                {
                    "requirement_id": item.requirement_id,
                    "category": item.category,
                    "mandatory": item.mandatory,
                    "status": item.status,
                    "owner_role": item.owner_role,
                    "disqualification_risk": item.disqualification_risk,
                    "due_date": item.due_date or "",
                    "evidence_count": len(item.available_evidence),
                    "requirement_text": item.requirement_text,
                    "recommended_action": item.recommended_action,
                }
            )

    risk_lines = [
        "# Risk Summary",
        "",
        f"- Opportunity: `{result.opportunity_id}`",
        f"- Requirements extracted: {len(result.requirements)}",
        f"- Blockers: {len(result.blockers)}",
        f"- Human review tasks: {len(result.review_tasks)}",
        f"- Evidence coverage: {result.evidence_coverage:.0%}",
        "",
        "## Blockers And Review Items",
    ]
    for task in result.review_tasks:
        risk_lines.append(
            f"- `{task.requirement_id}` [{task.priority}] {task.owner_role}: "
            f"{task.reason} Action: {task.required_action}"
        )
    (output_dir / "risk_summary.md").write_text("\n".join(risk_lines) + "\n", encoding="utf-8")

    draft_lines = ["# Draft Responses", ""]
    for requirement_id, response in result.draft_responses.items():
        draft_lines.extend([f"## {requirement_id}", "", response, ""])
    (output_dir / "draft_responses.md").write_text(
        "\n".join(draft_lines).rstrip() + "\n", encoding="utf-8"
    )

    queue_lines = ["# Human Review Queue", ""]
    for task in result.review_tasks:
        queue_lines.extend(
            [
                f"## {task.requirement_id}",
                "",
                f"- Owner: `{task.owner_role}`",
                f"- Priority: `{task.priority}`",
                f"- Reason: {task.reason}",
                f"- Required action: {task.required_action}",
                "",
            ]
        )
    (output_dir / "human_review_queue.md").write_text(
        "\n".join(queue_lines).rstrip() + "\n", encoding="utf-8"
    )
