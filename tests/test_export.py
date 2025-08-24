import csv
import json
from pathlib import Path

from export import Exporter


def make_project(tmp_path):
    # create metric map
    metric_map = {"TC-SC-110a.1": {"topic": 110, "sid": 11001}}
    with open(tmp_path / "metric_sid_map.json", "w", encoding="utf-8") as f:
        json.dump(metric_map, f)

    ann_dir = tmp_path / "annotations"
    ann_dir.mkdir()
    ann = {
        "metric_id": "TC-SC-110a.1",
        "annotations": [
            {
                "page": 1,
                "value": "2.5",
                "unit": "tCO2e",
                "complete": True,
                "bboxes": [{"x1": 1, "y1": 2, "x2": 3, "y2": 4}],
                "cat_ok": True,
                "unit_ok": True,
            }
        ],
    }
    with open(ann_dir / "TC-SC-110a.1.json", "w", encoding="utf-8") as f:
        json.dump(ann, f)
    return tmp_path


def test_export_tsmc5(tmp_path):
    project = make_project(tmp_path)
    exporter = Exporter(str(project))
    csv_path = exporter.export_tsmc5("uid", "cid")
    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    assert rows[1][0:4] == ["uid", "cid", "110", "11001"]


def test_export_full_and_pairs(tmp_path):
    project = make_project(tmp_path)
    exporter = Exporter(str(project))
    agg_path = exporter.export_full_report_agg()
    pair_path = exporter.export_single_page_pairs()
    assert Path(agg_path).exists()
    assert Path(pair_path).exists()
