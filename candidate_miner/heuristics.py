from __future__ import annotations

"""Rule-based candidate mining using regex and synonyms."""
from typing import Dict, List

from utils import find_numbers_and_units, text_has_synonym


def heuristic_candidates(metric_id: str, page_meta: Dict) -> List[Dict]:
    """Return heuristic candidates from page metadata.

    Parameters
    ----------
    metric_id: str
        SASB metric identifier.
    page_meta: Dict
        Dictionary with at least keys ``page`` and ``text``.
    """
    text = page_meta.get("text", "")
    results: List[Dict] = []
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
        
    return results
