# Devpost Submission Draft

## Project Title

BidPilot Qwen: Tender/RFP Autopilot Agent

## Tagline

Qwen Cloud agent that turns RFPs into evidence-grounded compliance matrices, draft responses, and human review queues.

## Track

Primary: Track 4, Autopilot Agent

Secondary fit: Track 3, Agent Society

## Project Description

BidPilot Qwen automates a real proposal-team workflow: reviewing complex RFPs, tenders, RFQs, and security questionnaires before a company decides whether and how to bid.

The agent ingests procurement documents and approved company evidence, extracts mandatory requirements and disqualification risks, searches for supporting evidence, drafts cited responses only when evidence exists, and routes legal, pricing, certification, delivery-date, and missing-evidence issues to accountable human reviewers.

The goal is simple: no evidence, no compliance claim.

## What It Does

- Extracts mandatory requirements, deadlines, submission instructions, scoring criteria, eligibility rules, and disqualification clauses.
- Uses Qwen Cloud to reason over ambiguous procurement language and classify risk.
- Searches approved company evidence before drafting any answer.
- Produces `requirements.json`, `compliance_matrix.csv`, `risk_summary.md`, `draft_responses.md`, and `human_review_queue.md`.
- Creates human-in-the-loop tasks for missing evidence, legal commitments, pricing, certifications, SLA, delivery dates, and low-confidence items.
- Keeps the workflow audit-friendly by separating extraction, evidence retrieval, reasoning, drafting, and review gates.

## How We Built It

The first version reuses our existing AWS/RFP proposal workflow material and adapts it to Qwen Cloud's Autopilot Agent track.

Architecture:

- Alibaba Cloud OSS stores incoming tender documents, approved evidence, and generated artifacts.
- Alibaba Cloud Function Compute hosts the backend handler.
- Qwen Cloud Chat Completions handles classification, reasoning, risk review, and response drafting.
- A multi-agent workflow decomposes the problem into intake, extraction, evidence search, compliance reasoning, drafting, human review, and export stages.
- Human review gates block unsafe claims before the final proposal package is used.

## Qwen Cloud Usage

The repo includes a Qwen Cloud client using the OpenAI-compatible endpoint:

```text
https://dashscope-intl.aliyuncs.com/compatible-mode/v1
```

The default model is configurable with `QWEN_MODEL`, with `qwen3.7-plus` as the default for the hackathon demo.

## Alibaba Cloud Deployment Proof

Code proof:

- `src/bidpilot_qwen/qwen_client.py`
- `src/bidpilot_qwen/alibaba_cloud_backend.py`
- `infra/alibaba-cloud/serverless-devs.yaml`

Public GitHub proof link after publishing:

```text
https://github.com/jasonlau111/qwen-tender-autopilot-agent/blob/main/src/bidpilot_qwen/alibaba_cloud_backend.py
```

## Demo Video URL

TODO: upload a public YouTube, Vimeo, or Facebook Video demo before final Devpost submission.

Suggested script: `docs/video-script.md`.

## Source Code

```text
https://github.com/jasonlau111/qwen-tender-autopilot-agent
```

## Try It Locally

```bash
python3 examples/run_demo.py
```

With Qwen Cloud:

```bash
export DASHSCOPE_API_KEY="your-qwen-cloud-key"
python3 examples/run_demo.py --qwen
```

## Built With

Qwen Cloud, Alibaba Cloud Function Compute, Alibaba Cloud OSS, Python, OpenAI-compatible Chat Completions API, procurement automation, RFP analysis, human-in-the-loop review.

## Future Work

- Deploy the Function Compute proof endpoint and record deployment proof.
- Add a lightweight reviewer UI.
- Add document parsing for PDF/DOCX/XLSX files.
- Add persistent evidence indexing with Alibaba Cloud OpenSearch or a vector database.
- Add reviewer audit trails and role-based access controls.
