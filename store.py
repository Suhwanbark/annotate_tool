"""Simple JSON based storage for annotations with autosave and backups."""
import os
import time
from typing import Dict, List

from utils import ensure_dir, read_json, write_json


class AnnotationStore:
    def __init__(self, project_dir: str):
        self.project_dir = project_dir
        self.ann_dir = os.path.join(project_dir, "annotations")
        ensure_dir(self.ann_dir)

    def _path(self, metric_id: str) -> str:
        safe = metric_id.replace("/", "_")
        return os.path.join(self.ann_dir, f"{safe}.json")

    def load(self, metric_id: str) -> Dict:
        path = self._path(metric_id)
        data = read_json(path)
        if not data:
            data = {"metric_id": metric_id, "annotations": []}
        return data

    def save(self, metric_data: Dict) -> None:
        path = self._path(metric_data["metric_id"])
        ensure_dir(os.path.dirname(path))
        if os.path.exists(path):
            ts = int(time.time())
            backup = f"{path}.{ts}.bak"
            os.replace(path, backup)
        write_json(path, metric_data)

    def add_annotation(self, metric_id: str, ann: Dict) -> None:
        data = self.load(metric_id)
        data["annotations"].append(ann)
        self.save(data)

