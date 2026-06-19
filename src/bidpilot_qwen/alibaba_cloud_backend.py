"""Alibaba Cloud Function Compute style backend for BidPilot Qwen.

This file is intentionally small so judges can inspect how the project connects
Qwen Cloud reasoning with an Alibaba Cloud backend shape.
"""

from __future__ import annotations

import json
import os
from io import BytesIO
from typing import Callable

from .workflow import run_workflow


def deployment_manifest() -> dict[str, object]:
    """Return the Alibaba Cloud services used by the deployment proof."""

    return {
        "runtime": "Alibaba Cloud Function Compute custom Python runtime",
        "model_api": {
            "service": "Qwen Cloud / DashScope",
            "base_url": os.getenv(
                "QWEN_BASE_URL",
                "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
            ),
            "model": os.getenv("QWEN_MODEL", "qwen3.7-plus"),
        },
        "storage": {
            "service": "Alibaba Cloud OSS",
            "bucket": os.getenv("ALIBABA_CLOUD_OSS_BUCKET", "bidpilot-qwen-demo"),
            "output_prefix": "outputs/",
        },
        "logs": {"service": "Alibaba Cloud Simple Log Service"},
        "region": os.getenv("ALIBABA_CLOUD_REGION", "ap-southeast-1"),
    }


def process_payload(payload: dict[str, object]) -> dict[str, object]:
    """Run the workflow from a JSON payload accepted by Function Compute."""

    opportunity_id = str(payload.get("opportunity_id") or "QWEN-RFP-2026-001")
    rfp_text = str(payload.get("rfp_text") or "")
    evidence_text = str(payload.get("evidence_text") or "")
    if not rfp_text or not evidence_text:
        return {
            "ok": False,
            "error": "rfp_text and evidence_text are required",
            "deployment": deployment_manifest(),
        }

    result = run_workflow(
        rfp_text=rfp_text,
        evidence_text=evidence_text,
        opportunity_id=opportunity_id,
        use_qwen=True,
    )
    return {
        "ok": True,
        "opportunity_id": result.opportunity_id,
        "requirements": len(result.requirements),
        "blockers": len(result.blockers),
        "human_review_tasks": len(result.review_tasks),
        "evidence_coverage": result.evidence_coverage,
        "deployment": deployment_manifest(),
    }


def handler(environ: dict[str, object], start_response: Callable) -> list[bytes]:
    """WSGI-compatible handler for Function Compute custom runtimes."""

    method = str(environ.get("REQUEST_METHOD") or "GET").upper()
    if method == "GET":
        body = {"ok": True, "deployment": deployment_manifest()}
        return _json_response(start_response, 200, body)

    length = int(str(environ.get("CONTENT_LENGTH") or "0") or "0")
    stream = environ.get("wsgi.input") or BytesIO()
    raw_body = stream.read(length) if hasattr(stream, "read") else b"{}"
    try:
        payload = json.loads(raw_body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return _json_response(start_response, 400, {"ok": False, "error": "invalid JSON"})
    return _json_response(start_response, 200, process_payload(payload))


def _json_response(start_response: Callable, status_code: int, body: dict[str, object]) -> list[bytes]:
    status_text = "OK" if status_code < 400 else "Bad Request"
    start_response(
        f"{status_code} {status_text}",
        [("Content-Type", "application/json; charset=utf-8")],
    )
    return [json.dumps(body, ensure_ascii=False).encode("utf-8")]
