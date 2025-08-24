import os
from utils import find_numbers_and_units, text_has_synonym, write_json, read_json


def test_find_numbers_and_units():
    text = "GHG emissions were 2.5 tCO2e and renewable energy reached 96.8 % in 2023"
    results = find_numbers_and_units(text)
    assert ("2.5", "tCO2e") in [(v, u) for v, u, _ in results]
    assert ("96.8", "%") in [(v, u) for v, u, _ in results]


def test_text_has_synonym():
    assert text_has_synonym("TC-SC-110a.1", "The company reports greenhouse gas emissions")
    assert not text_has_synonym("TC-SC-110a.1", "No related keywords here")


def test_read_write_json(tmp_path):
    path = tmp_path / "sample.json"
    data = {"a": 1}
    write_json(str(path), data)
    assert read_json(str(path)) == data
