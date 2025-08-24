"""Export utilities for annotation data."""
from __future__ import annotations

import csv
import json
import os
from typing import Dict, List

from pdf_loader import pdf_sha256
from utils import read_json


class Exporter:
    def __init__(self, project_dir: str):
        self.project_dir = project_dir
        self.ann_dir = os.path.join(project_dir, "annotations")
        self.export_dir = os.path.join(project_dir, "exports")
        os.makedirs(self.export_dir, exist_ok=True)
        with open(os.path.join(project_dir, "metric_sid_map.json"), "r", encoding="utf-8") as f:
            self.metric_map = json.load(f)

    def _iter_annotations(self):
        for fname in os.listdir(self.ann_dir):
            if not fname.endswith(".json"):
                continue
            data = read_json(os.path.join(self.ann_dir, fname))
            yield data

    def export_tsmc5(self, uid: str, cid: str = "tsmc") -> str:
        path = os.path.join(self.export_dir, "tsmc_5.csv")
        headers = [
            "uid",
            "cid",
            "topic",
            "sid",
            "page",
            "value",
            "unit",
            "complete",
            "x1",
            "y1",
            "x2",
            "y2",
        ]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for data in self._iter_annotations():
                m = self.metric_map.get(data["metric_id"], {})
                for ann in data.get("annotations", []):
                    bboxes = ann.get("bboxes") or [None]
                    for bbox in bboxes:
                        row = [
                            uid,
                            cid,
                            m.get("topic", 0),
                            m.get("sid", 0),
                            ann.get("page"),
                            ann.get("value", ""),
                            ann.get("unit", ""),
                            str(ann.get("complete", False)).lower(),
                        ]
                        if bbox:
                            row.extend([bbox.get("x1"), bbox.get("y1"), bbox.get("x2"), bbox.get("y2")])
                        else:
                            row.extend(["", "", "", ""])
                        writer.writerow(row)
        return path

    def export_full_report_agg(self) -> str:
        path = os.path.join(self.export_dir, "full_report_agg.csv")
        headers = ["metric", "pages", "cat_ok", "unit_ok"]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for data in self._iter_annotations():
                pages = sorted({ann["page"] for ann in data.get("annotations", [])})
                cat_ok = all(ann.get("cat_ok") for ann in data.get("annotations", []))
                unit_ok = all(ann.get("unit_ok") for ann in data.get("annotations", []))
                writer.writerow([data["metric_id"], " ".join(map(str, pages)), cat_ok, unit_ok])
        return path

    def export_single_page_pairs(self) -> str:
        path = os.path.join(self.export_dir, "single_page_pairs.csv")
        headers = ["metric", "page", "present", "cat_ok", "unit_ok"]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for data in self._iter_annotations():
                pages = sorted({ann["page"] for ann in data.get("annotations", [])})
                for p in pages:
                    anns = [a for a in data.get("annotations", []) if a["page"] == p]
                    writer.writerow(
                        [
                            data["metric_id"],
                            p,
                            bool(anns),
                            all(a.get("cat_ok") for a in anns),
                            all(a.get("unit_ok") for a in anns),
                        ]
                    )
        return path

    def export_metadata(self, company: str, pdf_path: str, year: int, lang: str, sasb_version: str) -> str:
        path = os.path.join(self.export_dir, "metadata.json")
        meta = {
            "company": company,
            "pdf_hash": pdf_sha256(pdf_path),
            "year": year,
            "lang": lang,
            "sasb_version": sasb_version,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)
        return path



def main():
    import argparse

    parser = argparse.ArgumentParser(description="Export annotations")
    parser.add_argument("--project", required=True)
    parser.add_argument("--uid", default="annotator")
    parser.add_argument("--company", default="tsmc")
    parser.add_argument("--pdf", required=True, help="original PDF path")
    parser.add_argument("--year", type=int, default=2024)
    parser.add_argument("--lang", default="en")
    parser.add_argument("--sasb_version", default="1.0")
    args = parser.parse_args()

    ex = Exporter(args.project)
    ex.export_tsmc5(args.uid, args.company)
    ex.export_full_report_agg()
    ex.export_single_page_pairs()
    ex.export_metadata(args.company, args.pdf, args.year, args.lang, args.sasb_version)


if __name__ == "__main__":
    main()

