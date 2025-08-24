"""Candidate mining modules."""
from __future__ import annotations

import json
from typing import Dict, List

import requests

from utils import find_numbers_and_units, text_has_synonym


class CandidateMiner:
    def __init__(self, config: Dict):
        self.config = config or {}

    # Heuristic miner
    def heuristic(self, metric_id: str, page_meta: Dict) -> List[Dict]:
        text = page_meta.get("text", "")
        results = []
        if not text_has_synonym(metric_id, text):
            return results
        for value, unit, _ in find_numbers_and_units(text):
            results.append(
                {
                    "page": page_meta["page"],
                    "value": value,
                    "unit": unit,
                    "category": "quantitative",
                    "bbox": None,
                }
            )
        return results

    # Optional LLM miner
    def llm(self, metric: str, page_text: str) -> List[Dict]:
        base = self.config.get("llm_base_url")
        key = self.config.get("api_key")
        model = self.config.get("llm_model")
        if not (base and key):
            return []
        url = f"{base}/responses"
        prompt = f"Extract metric {metric} candidates from the text. Return JSON list with keys page,value,unit,category,bbox. Text:{page_text[:2000]}"
        payload = {"model": model, "input": prompt}
        try:
            resp = requests.post(url, json=payload, headers={"Authorization": f"Bearer {key}"}, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            # expecting {'output': [{'content': '...json string...'}]}
            content = data.get("output", [{}])[0].get("content", "{}")
            return json.loads(content)
        except Exception:
            return []

