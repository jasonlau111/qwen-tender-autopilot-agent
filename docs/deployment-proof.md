# Alibaba Cloud Deployment Proof

The hackathon asks for proof of Alibaba Cloud deployment or a code link demonstrating Alibaba Cloud services and APIs.

This repo provides both a deployment path and code-level proof:

- Qwen Cloud API client: `src/bidpilot_qwen/qwen_client.py`
- Function Compute style backend: `src/bidpilot_qwen/alibaba_cloud_backend.py`
- Serverless deployment sketch: `infra/alibaba-cloud/serverless-devs.yaml`

## Environment Variables

```bash
export DASHSCOPE_API_KEY="your-qwen-cloud-api-key"
export QWEN_MODEL="qwen3.7-plus"
export QWEN_BASE_URL="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
export ALIBABA_CLOUD_OSS_BUCKET="your-oss-bucket"
export ALIBABA_CLOUD_REGION="ap-southeast-1"
```

## Local Handler Smoke Test

```bash
python3 examples/run_demo.py --qwen
```

## Deployment Recording Checklist

Record a short separate proof video showing:

1. Alibaba Cloud console with the Function Compute service.
2. Environment variables present without revealing secret values.
3. OSS bucket used for generated artifacts.
4. A request triggering the backend.
5. Generated output artifacts or logs.

Do not reveal access keys, API keys, tokens, cookies, or secret values in the recording.

## Public Proof Link

After GitHub publishing, use:

```text
https://github.com/jasonlau111/qwen-tender-autopilot-agent/blob/main/src/bidpilot_qwen/alibaba_cloud_backend.py
```
