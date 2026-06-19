# Qwen Cloud Hackathon Rules Alignment

Source pages:

- Hackathon overview: https://qwencloud-hackathon.devpost.com/
- Official rules: https://qwencloud-hackathon.devpost.com/rules
- Qwen Cloud OpenAI-compatible API docs: https://docs.qwencloud.com/api-reference/toolkitframework/openai-compatible/overview

## Key Dates

- Submission period: May 26, 2026 8:00 AM PT to July 9, 2026 2:00 PM PT.
- Judging period: July 10, 2026 to July 31, 2026.
- Winners announced: around August 7, 2026.

## Recommended Positioning

Primary track: Track 4, Autopilot Agent.

Reason: the project automates a real business workflow end to end: intake of ambiguous RFP/tender documents, requirement extraction, evidence retrieval, response drafting, and human review.

Secondary fit: Track 3, Agent Society.

Reason: the workflow is decomposed into multiple specialized agents with task division, disagreement handling, and stricter conflict resolution.

## Rule-To-Asset Mapping

| Qwen Cloud requirement | Our Qwen package answer | Reused AWS/RFP asset |
| --- | --- | --- |
| Build with Qwen models available on Qwen Cloud | `src/bidpilot_qwen/qwen_client.py` calls Qwen Cloud's OpenAI-compatible API with `DASHSCOPE_API_KEY` and `QWEN_MODEL`. | AWS prompt's Bedrock reasoning stage becomes Qwen Cloud reasoning and drafting. |
| Fit at least one track | `submission.md` and README position the project as Track 4 Autopilot Agent, with Track 3 as secondary. | AWS workflow already had document intake, compliance analysis, and review routing. |
| Public open-source repository with license | Repo includes `LICENSE`, README, source, examples, schema, docs, and instructions. | AWS prompt repo structure inspired the Qwen repo structure. |
| Proof of Alibaba Cloud deployment or service/API code | `alibaba_cloud_backend.py` and `infra/alibaba-cloud/serverless-devs.yaml` demonstrate Function Compute, OSS artifact paths, and Qwen Cloud API usage. | AWS architecture proof was converted from S3/Lambda/Bedrock to OSS/Function Compute/Qwen Cloud. |
| Architecture diagram | README and `docs/architecture.md` include Mermaid diagrams. | AWS service map converted to Alibaba Cloud service map. |
| About 3-minute demo video | `docs/video-script.md` provides the exact recording flow. | AWS sample input/output is reused as the demo scenario. |
| Text description of features/functionality | `submission.md` provides Devpost copy. | AWS submission text reworked for Qwen and Autopilot Agent track. |
| Judging: Innovation & AI Creativity 30% | Multi-agent workflow, strict evidence policy, human review gate, optional Qwen reasoning mode. | Existing "no evidence, no claim" principle. |
| Judging: Technical Depth & Engineering 30% | Modular Python package, Alibaba Cloud backend handler, output schemas, validation, tests. | AWS schema and output contracts. |
| Judging: Problem Value & Impact 25% | Solves real RFP response bottleneck for startups and small proposal teams. | Original Tender/RFP Compliance Copilot use case. |
| Judging: Presentation & Documentation 15% | README, architecture doc, judging map, video script, sample outputs. | Existing README/docs layout. |

## Gaps Before Final Submission

- A public YouTube, Vimeo, or Facebook Video demo URL is still required.
- A real Alibaba Cloud/Qwen Cloud deployment proof recording is recommended, even though the repo includes API/deployment code proof.
- If the Devpost form requires a live URL, deploy the Function Compute handler or provide the GitHub code proof link in the deployment proof field.
