"""CLI launcher for the annotation tool."""
from __future__ import annotations

import argparse
import json
import os

from pdf_loader import preprocess_pdf
from ui import AnnotationApp


def list_pdfs(data_dir: str):
    return [f for f in os.listdir(data_dir) if f.lower().endswith(".pdf")]


def main():
    parser = argparse.ArgumentParser(description="Lightweight annotation tool")
    parser.add_argument("--data_dir", required=True)
    parser.add_argument("--project", required=True, help="project workspace directory")
    parser.add_argument("--ocr", action="store_true", help="run OCR on pages")
    args = parser.parse_args()

    pdfs = list_pdfs(args.data_dir)
    if not pdfs:
        print("No PDFs found in", args.data_dir)
        return
    print("Available PDFs:")
    for i, name in enumerate(pdfs, start=1):
        print(f"{i}. {name}")
    choice = int(input("Select PDF number: ")) - 1
    pdf_path = os.path.join(args.data_dir, pdfs[choice])

    project_dir = args.project
    os.makedirs(project_dir, exist_ok=True)
    # copy metric_sid_map.json if not exists
    if not os.path.exists(os.path.join(project_dir, "metric_sid_map.json")):
        base_map = os.path.join(os.path.dirname(__file__), "metric_sid_map.json")
        if os.path.exists(base_map):
            import shutil

            shutil.copy(base_map, project_dir)

    pages_meta = preprocess_pdf(pdf_path, project_dir, ocr=args.ocr)

    # load config
    config_path = os.path.join(os.path.dirname(__file__), "config", "config.json")
    config = {}
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

    app = AnnotationApp(project_dir, pages_meta, config)
    app.run()


if __name__ == "__main__":
    main()

