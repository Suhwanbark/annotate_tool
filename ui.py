"""Tkinter-based manual verification UI."""
from __future__ import annotations

import json
import os
import tkinter as tk
from PIL import Image, ImageTk

from candidate_miner import CandidateMiner
from store import AnnotationStore


class AnnotationApp:
    def __init__(self, project_dir: str, pages_meta, config=None):
        self.project_dir = project_dir
        self.pages_meta = pages_meta
        self.store = AnnotationStore(project_dir)
        self.miner = CandidateMiner(config or {})

        self.root = tk.Tk()
        self.root.title("ESG Annotation Tool")

        # Metric list on the left
        self.metric_list = tk.Listbox(self.root, exportselection=False, width=25)
        self.metric_list.pack(side=tk.LEFT, fill=tk.Y)
        for metric_id in self._all_metrics():
            self.metric_list.insert(tk.END, metric_id)
        self.metric_list.bind("<<ListboxSelect>>", self.on_metric_select)

        # Canvas in the center
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="grey")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_canvas_press)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.current_boxes = []
        self.current_rect = None

        # Right panel for evidence
        self.panel = tk.Frame(self.root)
        self.panel.pack(side=tk.RIGHT, fill=tk.Y)

        self.candidate_list = tk.Listbox(self.panel, height=8)
        self.candidate_list.pack(fill=tk.X)

        self.value_var = tk.StringVar()
        tk.Label(self.panel, text="Value").pack(anchor="w")
        tk.Entry(self.panel, textvariable=self.value_var).pack(fill=tk.X)

        self.unit_var = tk.StringVar()
        tk.Label(self.panel, text="Unit").pack(anchor="w")
        tk.Entry(self.panel, textvariable=self.unit_var).pack(fill=tk.X)

        self.complete_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self.panel, text="Complete", variable=self.complete_var).pack(anchor="w")
        self.catok_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self.panel, text="Category OK", variable=self.catok_var).pack(anchor="w")
        self.unitok_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self.panel, text="Unit OK", variable=self.unitok_var).pack(anchor="w")

        tk.Button(self.panel, text="Save Annotation", command=self.save_current).pack(fill=tk.X)

        nav = tk.Frame(self.panel)
        nav.pack(fill=tk.X)
        tk.Button(nav, text="Prev", command=lambda: self.show_page(self.page_var.get() - 1)).pack(side=tk.LEFT)
        tk.Button(nav, text="Next", command=lambda: self.show_page(self.page_var.get() + 1)).pack(side=tk.LEFT)
        self.page_label = tk.Label(nav, text="1")
        self.page_label.pack(side=tk.LEFT)
        self.page_var = tk.IntVar(value=1)

        self.show_page(1)

    def _all_metrics(self):
        path = os.path.join(self.project_dir, "metric_sid_map.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return list(json.load(f).keys())
        return []

    # Canvas interactions
    def on_canvas_press(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.current_rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

    def on_canvas_drag(self, event):
        if self.current_rect:
            self.canvas.coords(self.current_rect, self.start_x, self.start_y, event.x, event.y)

    def on_canvas_release(self, event):
        if self.current_rect:
            x1, y1, x2, y2 = self.canvas.coords(self.current_rect)
            self.current_boxes.append({"x1": int(x1), "y1": int(y1), "x2": int(x2), "y2": int(y2)})
            self.current_rect = None

    def show_page(self, number: int):
        number = max(1, min(number, len(self.pages_meta)))
        self.page_var.set(number)
        self.page_label.config(text=str(number))
        meta = self.pages_meta[number - 1]
        img = Image.open(meta["image_path"])
        self.photo = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
        self.current_boxes = []

    def on_metric_select(self, event):
        metric_id = self.selected_metric()
        if not metric_id:
            return
        self.candidate_list.delete(0, tk.END)
        page_meta = self.pages_meta[self.page_var.get() - 1]
        for cand in self.miner.heuristic(metric_id, page_meta):
            self.candidate_list.insert(tk.END, f"{cand['value']} {cand['unit']}")
        data = self.store.load(metric_id)
        if data["annotations"]:
            ann = data["annotations"][-1]
            self.value_var.set(ann.get("value", ""))
            self.unit_var.set(ann.get("unit", ""))

    def selected_metric(self):
        sel = self.metric_list.curselection()
        if not sel:
            return None
        return self.metric_list.get(sel[0])

    def save_current(self):
        metric = self.selected_metric()
        if not metric:
            return
        ann = {
            "page": self.page_var.get(),
            "value": self.value_var.get(),
            "unit": self.unit_var.get(),
            "category": "quantitative",
            "complete": self.complete_var.get(),
            "bboxes": self.current_boxes[:],
            "cat_ok": self.catok_var.get(),
            "unit_ok": self.unitok_var.get(),
        }
        self.store.add_annotation(metric, ann)
        self.current_boxes = []

    def run(self):
        self.root.mainloop()

