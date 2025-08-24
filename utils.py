"""Utility helpers for annotation tool."""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple

# Regex patterns for numbers and common ESG units
NUMBER_RE = re.compile(r"\b\d[\d,\.]*\b")
UNIT_RE = re.compile(r"%(?!\w)|tCO2e|GJ|m³|m3|tons?|tonnes?|kg|kWh|MWh", re.IGNORECASE)

# Example metric synonym table. In practice this should be loaded from a file
# but keeping a small dictionary keeps the tool lightweight.
METRIC_SYNONYMS: Dict[str, List[str]] = {
    "TC-SC-110a.1": ["greenhouse gas", "ghg emissions"],
    "TC-SC-110a.2": ["renewable energy"],
    "TC-SC-130a.1": ["energy consumption", "energy use"],
}


def find_numbers_and_units(text: str) -> List[Tuple[str, str, Tuple[int, int]]]:
    """Return list of tuples: (number, unit, span)."""
    results: List[Tuple[str, str, Tuple[int, int]]] = []
    for m in NUMBER_RE.finditer(text):
        span = m.span()
        snippet = text[span[0] : span[1] + 20]
        unit_match = UNIT_RE.search(snippet)
        unit = unit_match.group(0) if unit_match else ""
        results.append((m.group(0), unit, span))
    return results


def text_has_synonym(metric_id: str, text: str) -> bool:
    syns = METRIC_SYNONYMS.get(metric_id, [])
    lowered = text.lower()
    return any(s in lowered for s in syns)


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def read_json(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: str, data: dict) -> None:
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


@dataclass
class BBox:
    x1: int
    y1: int
    x2: int
    y2: int

    def as_list(self) -> List[int]:
        return [self.x1, self.y1, self.x2, self.y2]

