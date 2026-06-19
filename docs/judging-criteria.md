# Judging Criteria Mapping

## Innovation & AI Creativity (30%)

BidPilot Qwen applies Qwen Cloud to a high-value business workflow instead of a generic chat assistant.

- Multi-agent proposal workflow with specialized responsibilities.
- Conflict policy: when agents disagree, the stricter risk interpretation wins.
- Evidence-first drafting: no evidence means no compliance claim.
- Human review gate converts ambiguous AI outputs into accountable proposal tasks.
- Optional Qwen Cloud reasoning can be layered over deterministic validators.

## Technical Depth & Engineering (30%)

- Modular Python package with source code, schema, examples, and tests.
- Qwen Cloud API client using the OpenAI-compatible endpoint.
- Alibaba Cloud Function Compute style handler.
- Serverless deployment sketch for Function Compute and OSS.
- Deterministic fallback demo for judges without credentials.
- Structured output contract for JSON, CSV, and Markdown artifacts.
- Error-tolerant design: missing credentials do not break the local demo.

## Problem Value & Impact (25%)

RFP response is a real operational bottleneck for startups, SaaS vendors, and small proposal teams. A single missed mandatory clause can disqualify a bid. A single unsupported compliance claim can create legal or customer trust risk.

BidPilot Qwen helps teams:

- shorten first-pass RFP review
- identify blockers early
- keep proposals evidence-grounded
- reduce hallucinated compliance statements
- make bid/no-bid decisions with clearer risk ownership

## Presentation & Documentation (15%)

The repo includes:

- README with quickstart and architecture diagram
- Devpost submission draft
- Qwen rules alignment
- architecture documentation
- deployment proof notes
- video script
- sample input and generated outputs
- tests and validation commands

## Demo Narrative

The 3-minute demo should show:

1. A messy RFP snippet and evidence bundle.
2. Local run with `python3 examples/run_demo.py`.
3. Generated compliance matrix, blockers, and draft responses.
4. Qwen/Alibaba Cloud integration files.
5. The human review queue proving the system does not auto-approve risky claims.
