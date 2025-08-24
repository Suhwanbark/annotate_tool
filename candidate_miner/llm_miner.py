"""LLM-powered candidate mining via OpenAI-compatible Responses API."""
from __future__ import annotations

import requests
from typing import Dict, List

from .prompts import build_candidate_payload


def llm_candidates(metric: Dict, page_text: str, config: Dict) -> List[Dict]:
    """Query external LLM for candidate annotations.

    Parameters
    ----------
    metric: Dict
        Metric metadata such as code, title, expected units and category.
    page_text: str
        Text content of the page.
    config: Dict
        Configuration containing ``llm_base_url``, ``api_key`` and ``llm_model``.
    """
    base = config.get("llm_base_url")
    key = config.get("api_key")
    model = config.get("llm_model")
    if not (base and key and model):
        return []

    payload = build_candidate_payload(model, metric, page_text)
    url = f"{base}/responses"
    headers = {"Authorization": f"Bearer {key}"}

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("candidates", [])
    except Exception:
        return []
