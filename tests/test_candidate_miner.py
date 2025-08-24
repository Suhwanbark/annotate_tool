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
                return {"output": [{"content": '[{"page":1,"value":"1","unit":"%","category":"x"}]'}]}

        return Resp()

    monkeypatch.setattr(requests, "post", fake_post)
    miner = CandidateMiner({"llm_base_url": "http://x", "api_key": "k", "llm_model": "m"})
    res = miner.llm("metric", "text")
    assert res and res[0]["unit"] == "%"
