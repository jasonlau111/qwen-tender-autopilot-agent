# Three-Minute Demo Script

Target length: 2:45 to 3:00.

## 0:00-0:20 Problem

"Proposal teams lose days reading RFPs and matching requirements to approved company evidence. If they miss a mandatory clause or invent a compliance claim, they can lose the bid or create legal risk."

Show `examples/sample-input.md`.

## 0:20-0:45 Solution

"BidPilot Qwen is an Autopilot Agent on Qwen Cloud. It extracts requirements, finds evidence, drafts cited answers, and blocks risky items for human review."

Show README architecture diagram.

## 0:45-1:25 Live Run

Run:

```bash
python3 examples/run_demo.py
```

Optional Qwen mode:

```bash
DASHSCOPE_API_KEY=... python3 examples/run_demo.py --qwen
```

Show generated outputs in `examples/expected-outputs/`.

## 1:25-2:10 Key Outputs

Open:

- `requirements.json`
- `compliance_matrix.csv`
- `risk_summary.md`
- `draft_responses.md`
- `human_review_queue.md`

Narration:

"The agent found mandatory clauses, assigned owner roles, checked evidence, and created a blocker where evidence was missing. It drafted only when approved evidence was present."

## 2:10-2:35 Qwen And Alibaba Cloud

Show:

- `src/bidpilot_qwen/qwen_client.py`
- `src/bidpilot_qwen/alibaba_cloud_backend.py`
- `infra/alibaba-cloud/serverless-devs.yaml`

Narration:

"The Qwen client uses the Qwen Cloud OpenAI-compatible endpoint. The backend is designed for Alibaba Cloud Function Compute with OSS artifact storage."

## 2:35-3:00 Close

"The rule is no evidence, no claim. BidPilot Qwen turns an ambiguous RFP into an auditable proposal workflow with Qwen reasoning and human checkpoints."
