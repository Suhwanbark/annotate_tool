from store import AnnotationStore


def test_add_and_load(tmp_path):
    store = AnnotationStore(str(tmp_path))
    ann = {"page": 1, "value": "1"}
    store.add_annotation("metric", ann)
    data = store.load("metric")
    assert data["annotations"][0]["value"] == "1"

    store.add_annotation("metric", {"page": 2, "value": "2"})
    backups = list((tmp_path / "annotations").glob("metric.json.*.bak"))
    assert backups  # backup created on second save
