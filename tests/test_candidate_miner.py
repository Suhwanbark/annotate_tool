import requests
import requests

from candidate_miner import CandidateMiner


def test_heuristic_mining():
    miner = CandidateMiner({})
    page = {"page": 1, "text": "Greenhouse gas emissions totalled 2.5 tCO2e"}
    res = miner.heuristic("TC-SC-110a.1", page)
    assert res and res[0]["value"] == "2.5"


def test_llm_mining(monkeypatch):
    def fake_post(url, json, headers, timeout):
        class Resp:
            def raise_for_status(self):
                pass

            def json(self):
                return {
                    "candidates": [
                        {
                            "page": 1,
                            "score": 0.9,
                            "category_pred": "discussion",
                            "unit_pred": "%",
                        }
                    ]
                }

        return Resp()

    monkeypatch.setattr(requests, "post", fake_post)
    miner = CandidateMiner({"llm_base_url": "http://x", "api_key": "k", "llm_model": "m"})
    metric = {
        "metric_code": "metric",
        "metric_title": "",
        "expected_category": "quantitative",
        "expected_units": ["%"],
        "page_no": 1,
    }
    res = miner.llm(metric, "text")
    assert res and res[0]["unit_pred"] == "%"
