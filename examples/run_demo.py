#!/usr/bin/env python3
"""Run the BidPilot Qwen sample workflow."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from bidpilot_qwen.workflow import export_result, run_workflow  # noqa: E402


def _section(markdown: str, heading: str) -> str:
    pattern = re.compile(
        rf"^## {re.escape(heading)}\n(?P<body>.*?)(?=^## |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(markdown)
    if not match:
        raise ValueError(f"Missing section: {heading}")
    return match.group("body").strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--qwen", action="store_true", help="Call Qwen Cloud when configured")
    parser.add_argument(
        "--output-dir",
        default=str(ROOT / "examples" / "expected-outputs"),
        help="Directory for generated artifacts",
    )
    args = parser.parse_args()

    sample = (ROOT / "examples" / "sample-input.md").read_text(encoding="utf-8")
    opportunity = _section(sample, "Opportunity")
    rfp_text = _section(sample, "RFP Text")
    evidence_text = _section(sample, "Approved Evidence Bundle")
    opportunity_id_match = re.search(r"Opportunity ID:\s*(\S+)", opportunity)
    opportunity_id = opportunity_id_match.group(1) if opportunity_id_match else "QWEN-RFP-2026-001"

    result = run_workflow(
        rfp_text=rfp_text,
        evidence_text=evidence_text,
        opportunity_id=opportunity_id,
        use_qwen=args.qwen,
    )
    export_result(result, Path(args.output_dir))

    print(f"Opportunity: {result.opportunity_id}")
    print(f"Requirements extracted: {len(result.requirements)}")
    print(f"Blockers: {len(result.blockers)}")
    print(f"Human review tasks: {len(result.review_tasks)}")
    print(f"Evidence coverage: {result.evidence_coverage:.0%}")
    print(f"Artifacts: {Path(args.output_dir).resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
