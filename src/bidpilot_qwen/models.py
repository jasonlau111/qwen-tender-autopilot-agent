"""Data models for BidPilot Qwen workflow artifacts."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class EvidenceHit:
    evidence_id: str
    source_document: str
    source_section: str
    relevance_score: float
    quote_or_summary: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Requirement:
    opportunity_id: str
    requirement_id: str
    category: str
    requirement_text: str
    normalized_requirement: str
    mandatory: bool
    disqualification_risk: str
    source_document: str
    source_section: str
    confidence: float
    due_date: str | None
    owner_role: str
    evidence_needed: list[str]
    available_evidence: list[EvidenceHit] = field(default_factory=list)
    status: str = "not_started"
    recommended_action: str = ""
    review_notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["available_evidence"] = [
            evidence.to_dict() for evidence in self.available_evidence
        ]
        return payload


@dataclass
class ReviewTask:
    requirement_id: str
    owner_role: str
    priority: str
    reason: str
    required_action: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class WorkflowResult:
    opportunity_id: str
    requirements: list[Requirement]
    review_tasks: list[ReviewTask]
    draft_responses: dict[str, str]
    agent_trace: list[str]

    @property
    def blockers(self) -> list[Requirement]:
        return [item for item in self.requirements if item.status == "blocker"]

    @property
    def evidence_coverage(self) -> float:
        if not self.requirements:
            return 0.0
        with_evidence = sum(1 for item in self.requirements if item.available_evidence)
        return round(with_evidence / len(self.requirements), 2)
