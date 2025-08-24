"""Candidate mining package providing heuristics and LLM helpers."""
from __future__ import annotations

from typing import Dict, List

from .heuristics import heuristic_candidates
from .llm_miner import llm_candidates


class CandidateMiner:
    def __init__(self, config: Dict | None = None):
        self.config = config or {}

    def heuristic(self, metric_id: str, page_meta: Dict) -> List[Dict]:
        return heuristic_candidates(metric_id, page_meta)

    def llm(self, metric: Dict, page_text: str) -> List[Dict]:
        """Return candidates from external LLM."""
        return llm_candidates(metric, page_text, self.config)

    def combined(self, metric_id: str, metric: Dict, page_meta: Dict) -> List[Dict]:
        """Merge heuristic and LLM candidates sorted by score."""
        results = []
        for h in heuristic_candidates(metric_id, page_meta):
            h.setdefault("score", 0.5)
            results.append(h)
        results.extend(llm_candidates(metric, page_meta.get("text", ""), self.config))
        return sorted(results, key=lambda x: x.get("score", 0), reverse=True)
