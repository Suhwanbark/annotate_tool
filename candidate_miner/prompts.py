"""Prompt templates for LLM-based mining and draft annotations."""
from __future__ import annotations

from typing import Dict, List

CANDIDATE_SYSTEM = (
    "You are an assistant that finds SASB metrics in ESG report pages. "
    "Always output strict JSON."
)


def build_candidate_payload(model: str, metric: Dict, page_text: str) -> Dict:
    """Return request payload for candidate mining."""
    user_content = {
        "metric_code": metric.get("metric_code", ""),
        "metric_title": metric.get("metric_title", ""),
        "expected_category": metric.get("expected_category", ""),
        "expected_units": metric.get("expected_units", []),
        "page_no": metric.get("page_no"),
        "page_text": page_text,
    }
    schema = {
        "type": "object",
        "properties": {
            "candidates": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "page": {"type": "integer"},
                        "score": {"type": "number"},
                        "category_pred": {
                            "type": "string",
                            "enum": ["quantitative", "discussion"],
                        },
                        "unit_pred": {"type": "string"},
                        "value": {"type": "string"},
                        "spans": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "x1": {"type": "number"},
                                    "y1": {"type": "number"},
                                    "x2": {"type": "number"},
                                    "y2": {"type": "number"},
                                },
                            },
                        },
                        "rationale": {"type": "string"},
                    },
                    "required": ["page", "score", "category_pred"],
                },
            }
        },
        "required": ["candidates"],
    }
    return {
        "model": model,
        "input": [
            {"role": "system", "content": CANDIDATE_SYSTEM},
            {"role": "user", "content": user_content},
        ],
        "response_format": {"type": "json_schema", "json_schema": {"name": "CandidateList", "schema": schema}},
    }


DRAFT_SYSTEM = (
    "You assist annotators by creating draft annotations from ESG pages."
)


def build_draft_messages(metric: Dict, page_text: str) -> List[Dict]:
    """Return messages for draft annotation suggestion."""
    user = f'''Metric: {metric.get('metric_code', '')} - {metric.get('metric_title', '')}
Page {metric.get('page_no')} text:
"""{page_text}"""

TASK:
Suggest draft annotation fields:
- value (if any quantitative number appears)
- unit (best guess from text)
- category (quantitative or discussion)
- rationale (short reason)
- spans (approximate bbox coordinates if possible)
Output strictly in JSON.
'''
    return [
        {"role": "system", "content": DRAFT_SYSTEM},
        {"role": "user", "content": user},
    ]
