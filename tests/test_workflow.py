"""Tests for the BidPilot Qwen workflow."""

from __future__ import annotations

import unittest

from bidpilot_qwen.workflow import run_workflow


class WorkflowTest(unittest.TestCase):
    def test_mandatory_missing_evidence_becomes_blocker(self) -> None:
        result = run_workflow(
            rfp_text="The vendor must submit pricing in the provided spreadsheet.",
            evidence_text="Evidence A: Security Overview\nSOC 2 report is available.",
            opportunity_id="TEST-1",
        )
        self.assertEqual(len(result.requirements), 1)
        self.assertEqual(result.requirements[0].status, "blocker")
        self.assertEqual(len(result.review_tasks), 1)

    def test_supported_requirement_gets_evidence(self) -> None:
        result = run_workflow(
            rfp_text="The solution must support English and Chinese interactions.",
            evidence_text=(
                "Evidence A: Product Localization Guide, section 1.4\n"
                "The assistant supports English and Chinese user interactions."
            ),
            opportunity_id="TEST-2",
        )
        self.assertEqual(len(result.requirements[0].available_evidence), 1)
        self.assertIn(result.requirements[0].status, {"draft_ready", "needs_review"})


if __name__ == "__main__":
    unittest.main()
