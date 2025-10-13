#!/usr/bin/env python3
"""PyQt5를 사용한 ESG 주석 도구"""

import sys
import os
import time
import json
import shutil
import csv
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, 
                             QVBoxLayout, QListWidget, QLabel, QLineEdit, 
                             QPushButton, QCheckBox, QScrollArea, QSplitter,
                             QTextEdit, QFrame, QListWidgetItem)
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QMouseEvent
from PIL import Image

class DraggableImageLabel(QLabel):
    """드래그 가능한 이미지 라벨"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.start_point = QPoint()
        self.end_point = QPoint()
        self.boxes = []
        self.current_box = None
        self.drawing = False
        
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.start_point = event.pos()
            self.drawing = True
            
    def mouseMoveEvent(self, event: QMouseEvent):
        if self.drawing:
            self.end_point = event.pos()
            self.update()  # 화면 다시 그리기
            
    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and self.drawing:
            self.end_point = event.pos()
            self.drawing = False
            
            # 박스 추가
            rect = QRect(self.start_point, self.end_point).normalized()
            if rect.width() > 10 and rect.height() > 10:  # 최소 크기 체크
                self.boxes.append(rect)
                print(f"박스 추가됨: {rect.x()}, {rect.y()}, {rect.width()}, {rect.height()}")
            
            self.update()
            
    def paintEvent(self, event):
        super().paintEvent(event)
        
        painter = QPainter(self)
        pen = QPen(QColor(255, 0, 0), 2)  # 빨간색 선
        painter.setPen(pen)
        
        # 저장된 박스들 그리기
        for box in self.boxes:
            painter.drawRect(box)
            
        # 현재 그리고 있는 박스 그리기
        if self.drawing:
            current_rect = QRect(self.start_point, self.end_point).normalized()
            painter.drawRect(current_rect)
            
    def clear_boxes(self):
        """모든 박스 지우기"""
        self.boxes.clear()
        self.update()
        
    def get_boxes(self):
        """박스 목록을 딕셔너리 형태로 반환"""
        result = []
        for box in self.boxes:
            x, y, width, height = box.x(), box.y(), box.width(), box.height()
            result.append({
                "x1": x,
                "y1": y, 
                "x2": x + width,
                "y2": y + height
            })
        return result

class ESGAnnotationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ESG 주석 도구 (고해상도)")
        self.setGeometry(100, 100, 1600, 1000)  # 윈도우 크기 확대

        # 메트릭 매핑 딕셔너리 (display_text → metric_id)
        self.display_to_metric = {}

        # 현재 선택된 메트릭 ID 저장
        self.current_selected_metric = None

        # 페이지별 메트릭 매핑 (metric_id → [pages])
        self.metric_page_mapping = {}
        self.load_metric_page_mapping()

        # 메인 위젯
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # 메인 레이아웃 - 수평 분할
        splitter = QSplitter(Qt.Horizontal)
        main_layout = QHBoxLayout()
        main_layout.addWidget(splitter)
        main_widget.setLayout(main_layout)
        
        # 왼쪽 패널 - 메트릭 목록
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # 중앙 패널 - 이미지 뷰어
        center_panel = self.create_center_panel()
        splitter.addWidget(center_panel)
        
        # 오른쪽 패널 - 주석 입력
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # 분할 비율 설정 (좌측 패널 너비 확대)
        splitter.setSizes([400, 900, 350])  # 좌측 패널: 250 → 400
        
        print("PyQt5 GUI 초기화 완료!")
        
    def load_metrics_from_json(self):
        """JSON 파일에서 메트릭 로드"""
        try:
            metric_file = os.path.join("../new_project", "metric_sid_map.json")
            with open(metric_file, 'r', encoding='utf-8') as f:
                metrics = json.load(f)

            self.metric_list.clear()
            self.display_to_metric.clear()

            for metric_id, info in metrics.items():
                # topic, sid, category, unit 가져오기
                topic = info.get('topic', 'Unknown Topic')
                sid = info.get('sid', 'Unknown SID')
                category = info.get('category', 'N/A')
                unit = info.get('unit', 'N/A')

                # SID 포맷팅: 너무 긴 경우 적절히 줄바꿈
                # 약 50자마다 공백에서 줄바꿈
                formatted_sid = self.format_long_text(sid, max_length=60)

                # 표시 텍스트: topic, sid, category, unit 모두 표시
                display_text = f"{topic}\n{formatted_sid}\nCategory: {category} | Unit: {unit}"

                # 매핑 딕셔너리에 저장
                self.display_to_metric[display_text] = metric_id

                # 리스트 아이템 생성
                item = QListWidgetItem(display_text)

                # 툴팁 추가 (metric_id도 표시)
                tooltip_text = f"📋 {topic}\n\n📝 {sid}\n\n📂 Category: {category}\n📏 Unit: {unit}\n\n🔖 {metric_id}"
                item.setToolTip(tooltip_text)

                self.metric_list.addItem(item)
                print(f"메트릭 로드됨: {metric_id} → {topic}")

        except Exception as e:
            print(f"메트릭 로드 실패: {e}")
            import traceback
            traceback.print_exc()

    def format_long_text(self, text, max_length=60):
        """긴 텍스트를 적절한 길이로 줄바꿈"""
        if len(text) <= max_length:
            return text

        words = text.split()
        lines = []
        current_line = []
        current_length = 0

        for word in words:
            word_length = len(word)
            # 현재 줄에 단어를 추가했을 때 길이 체크
            if current_length + word_length + len(current_line) <= max_length:
                current_line.append(word)
                current_length += word_length
            else:
                # 현재 줄이 비어있지 않으면 저장
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_length = word_length

        # 마지막 줄 추가
        if current_line:
            lines.append(' '.join(current_line))

        return '\n'.join(lines)

    def load_metric_page_mapping(self):
        """metric_page_mapping.json 로드"""
        try:
            mapping_file = os.path.join("../new_project", "metric_page_mapping.json")
            if os.path.exists(mapping_file):
                with open(mapping_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.metric_page_mapping = data.get("metric_page_mapping", {})
                print(f"✅ 메트릭-페이지 매핑 로드 완료: {len(self.metric_page_mapping)}개 메트릭")
            else:
                print(f"⚠️  메트릭-페이지 매핑 파일 없음: {mapping_file}")
                print("   heuristic_analysis.ipynb를 실행하여 생성하세요.")
        except Exception as e:
            print(f"❌ 메트릭-페이지 매핑 로드 실패: {e}")
            import traceback
            traceback.print_exc()

    def get_likely_metrics_for_page(self, page_num):
        """특정 페이지에서 likely한 메트릭 리스트 반환"""
        likely_metrics = []
        for metric_id, pages in self.metric_page_mapping.items():
            if page_num in pages:
                likely_metrics.append(metric_id)
        return likely_metrics

    def update_likely_metrics_display(self):
        """현재 페이지의 likely 메트릭 표시 업데이트"""
        likely_metrics = self.get_likely_metrics_for_page(self.current_page)

        if not likely_metrics:
            # 관련 메트릭이 없는 경우
            self.likely_metrics_label.setText("📌 이 페이지와 관련된 메트릭: 없음")
            self.likely_metrics_label.setStyleSheet("""
                padding: 10px;
                background-color: #f5f5f5;
                border: 2px solid #ccc;
                border-radius: 5px;
                font-size: 11px;
                color: #666;
            """)
        else:
            # 관련 메트릭이 있는 경우
            # metric_sid_map.json에서 topic과 sid 가져오기
            metric_file = os.path.join("../new_project", "metric_sid_map.json")
            try:
                with open(metric_file, 'r', encoding='utf-8') as f:
                    metrics = json.load(f)

                metric_details = []
                for metric_id in likely_metrics:
                    metric_info = metrics.get(metric_id, {})
                    topic = metric_info.get('topic', metric_id)
                    sid = metric_info.get('sid', '')

                    # SID를 적절히 줄바꿈 (50자마다)
                    formatted_sid = self.format_long_text(sid, max_length=80)

                    metric_details.append(f"• {topic}\n  {formatted_sid}")

                display_text = f"📌 이 페이지와 관련된 메트릭 ({len(likely_metrics)}개):\n\n" + "\n\n".join(metric_details)
                self.likely_metrics_label.setText(display_text)
                self.likely_metrics_label.setStyleSheet("""
                    padding: 12px;
                    background-color: #fff9e6;
                    border: 2px solid #ffa726;
                    border-radius: 5px;
                    font-size: 11px;
                    color: #663c00;
                    line-height: 1.5;
                """)
            except Exception as e:
                print(f"❌ 메트릭 정보 로드 실패: {e}")
                self.likely_metrics_label.setText(f"📌 이 페이지와 관련된 메트릭: {len(likely_metrics)}개")

    def create_left_panel(self):
        """왼쪽 메트릭 리스트 패널"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Box)
        panel.setStyleSheet("background-color: #f0f4f8;")  # 연한 회색-파랑

        layout = QVBoxLayout()

        # 제목
        title = QLabel("메트릭 목록")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            margin: 10px;
            color: #1a365d;
            background-color: white;
            padding: 8px;
            border-radius: 5px;
        """)
        layout.addWidget(title)

        # 메트릭 리스트 - JSON 파일에서 로드
        self.metric_list = QListWidget()

        # Word wrap 활성화 (긴 텍스트 자동 줄바꿈)
        self.metric_list.setWordWrap(True)
        self.metric_list.setResizeMode(QListWidget.Adjust)

        # 리스트 스타일 개선 - 여러 줄 텍스트 지원
        self.metric_list.setStyleSheet("""
            QListWidget {
                font-size: 11px;
                padding: 5px;
                background-color: #f0f4f8;
                border: none;
            }
            QListWidget::item {
                padding: 12px 10px;
                margin: 4px;
                border-radius: 6px;
                background-color: white;
                color: #2d3748;
                border: 1px solid #e2e8f0;
                line-height: 1.6;
            }
            QListWidget::item:hover {
                background-color: #fff4e6;
                border: 1px solid #ffa726;
                color: #e65100;
            }
            QListWidget::item:selected {
                background-color: #2563eb;
                color: white;
                font-weight: bold;
                border: 1px solid #1e40af;
            }
        """)

        self.load_metrics_from_json()
        self.metric_list.itemClicked.connect(self.on_metric_selected)
        layout.addWidget(self.metric_list)
        
        # 선택된 메트릭 표시
        self.selected_metric_label = QLabel("선택된 메트릭: 없음")
        self.selected_metric_label.setStyleSheet("""
            font-weight: bold;
            color: #1a365d;
            padding: 8px;
            background-color: white;
            border: 2px solid #2563eb;
            border-radius: 5px;
            font-size: 12px;
        """)
        layout.addWidget(self.selected_metric_label)
        
        panel.setLayout(layout)
        return panel
        
    def create_center_panel(self):
        """중앙 이미지 뷰어 패널"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Box)
        panel.setStyleSheet("background-color: white;")
        
        layout = QVBoxLayout()
        
        # 제목
        title = QLabel("PDF 페이지")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # 스크롤 가능한 이미지 영역 (고해상도 지원)
        scroll_area = QScrollArea()
        scroll_area.setMinimumSize(900, 700)  # 스크롤 영역 확대
        self.image_label = DraggableImageLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid gray; background-color: white;")
        self.image_label.setText("🖼️ 고해상도 이미지로 로딩됩니다...")
        self.image_label.setMinimumSize(800, 600)  # 이미지 라벨 확대
        
        scroll_area.setWidget(self.image_label)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        # 이 페이지와 관련된 메트릭 표시 (스크롤 가능)
        metrics_scroll = QScrollArea()
        metrics_scroll.setMaximumHeight(150)  # 최대 높이 제한
        metrics_scroll.setWidgetResizable(True)
        metrics_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        metrics_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.likely_metrics_label = QLabel("📌 이 페이지와 관련된 메트릭: 분석 중...")
        self.likely_metrics_label.setStyleSheet("""
            padding: 10px;
            background-color: #fff9e6;
            border: 2px solid #ffa726;
            border-radius: 5px;
            font-size: 11px;
            color: #663c00;
        """)
        self.likely_metrics_label.setWordWrap(True)

        metrics_scroll.setWidget(self.likely_metrics_label)
        metrics_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)

        layout.addWidget(metrics_scroll)

        # 페이지 네비게이션
        nav_layout = QHBoxLayout()
        self.prev_btn = QPushButton("◀ 이전")
        self.prev_btn.setMinimumHeight(35)
        self.prev_btn.setStyleSheet("QPushButton { font-size: 14px; font-weight: bold; padding: 5px; }")
        
        self.next_btn = QPushButton("다음 ▶")
        self.next_btn.setMinimumHeight(35)
        self.next_btn.setStyleSheet("QPushButton { font-size: 14px; font-weight: bold; padding: 5px; }")
        
        self.page_label = QLabel("페이지 1")
        self.page_label.setStyleSheet("QLabel { font-size: 14px; font-weight: bold; color: black; background-color: white; padding: 8px; border: 1px solid gray; }")
        self.page_label.setAlignment(Qt.AlignCenter)
        
        # 페이지 관련 변수 초기화
        self.current_page = 1
        self.total_pages = self.count_total_pages()
        
        # 이벤트 연결
        self.prev_btn.clicked.connect(self.prev_page)
        self.next_btn.clicked.connect(self.next_page)
        
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.next_btn)
        nav_layout.addWidget(self.page_label)
        nav_layout.addStretch()
        
        layout.addLayout(nav_layout)
        
        # 초기 페이지 로드
        self.load_current_page()
        
        panel.setLayout(layout)
        return panel
        
    def create_right_panel(self):
        """오른쪽 주석 입력 패널"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Box)
        panel.setStyleSheet("background-color: lightcoral;")
        
        layout = QVBoxLayout()
        
        # 제목
        title = QLabel("주석 입력")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # 후보 목록
        candidate_label = QLabel("후보 목록:")
        candidate_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(candidate_label)
        
        self.candidate_list = QListWidget()
        self.candidate_list.setMaximumHeight(100)
        self.candidate_list.itemClicked.connect(self.on_candidate_selected)
        layout.addWidget(self.candidate_list)
        
        # 값 입력
        value_label = QLabel("값:")
        value_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(value_label)
        
        self.value_input = QLineEdit()
        layout.addWidget(self.value_input)
        
        # 단위 입력
        unit_label = QLabel("단위:")
        unit_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(unit_label)
        
        self.unit_input = QLineEdit()
        layout.addWidget(self.unit_input)
        
        # 체크박스들
        self.complete_cb = QCheckBox("완료")
        self.category_cb = QCheckBox("카테고리 OK")
        self.unit_cb = QCheckBox("단위 OK")
        
        layout.addWidget(self.complete_cb)
        layout.addWidget(self.category_cb)
        layout.addWidget(self.unit_cb)
        
        # 버튼들
        self.save_btn = QPushButton("💾 주석 저장")
        self.save_btn.clicked.connect(self.save_annotation)
        self.save_btn.setStyleSheet("QPushButton { background-color: #27ae60; color: white; font-weight: bold; font-size: 14px; padding: 8px; }")
        layout.addWidget(self.save_btn)
        
        # 저장 상태 표시
        self.save_status = QLabel("저장 준비됨")
        self.save_status.setAlignment(Qt.AlignCenter)
        self.save_status.setStyleSheet("padding: 5px; background-color: #f8f9fa; border: 1px solid #dee2e6;")
        layout.addWidget(self.save_status)
        
        self.load_img_btn = QPushButton("이미지 로드")
        self.load_img_btn.clicked.connect(self.load_image)
        layout.addWidget(self.load_img_btn)
        
        self.clear_boxes_btn = QPushButton("박스 모두 지우기")
        self.clear_boxes_btn.clicked.connect(self.clear_all_boxes)
        self.clear_boxes_btn.setStyleSheet("QPushButton { background-color: #ff6b6b; color: white; font-weight: bold; }")
        layout.addWidget(self.clear_boxes_btn)
        
        # 내보내기 버튼
        self.export_btn = QPushButton("📊 CSV 내보내기")
        self.export_btn.setStyleSheet("QPushButton { background-color: #3498db; color: white; font-weight: bold; padding: 8px; }")
        self.export_btn.clicked.connect(self.export_to_csv)
        layout.addWidget(self.export_btn)

        # 종료 버튼 추가
        self.quit_btn = QPushButton("🚪 프로그램 종료")
        self.quit_btn.clicked.connect(self.close_application)
        self.quit_btn.setStyleSheet("QPushButton { background-color: #666; color: white; font-weight: bold; font-size: 14px; padding: 8px; }")
        layout.addWidget(self.quit_btn)
        
        layout.addStretch()
        
        panel.setLayout(layout)
        return panel
        
    def on_metric_selected(self, item):
        """메트릭 선택 시"""
        display_text = item.text()  # "Product Security\nDescription of..." 형태

        # 매핑 딕셔너리에서 메트릭 ID 가져오기
        metric_id = self.display_to_metric.get(display_text, "Unknown")

        # topic만 추출 (첫 번째 줄)
        topic = display_text.split('\n')[0]

        print(f"✅ 메트릭 선택됨: {metric_id}")
        print(f"   Topic: {topic}")

        # 선택된 메트릭 라벨 업데이트
        self.selected_metric_label.setText(f"✓ 선택됨: {topic}")
        self.selected_metric_label.setStyleSheet("""
            font-weight: bold;
            color: #059669;
            padding: 8px;
            background-color: #d1fae5;
            border: 2px solid #10b981;
            border-radius: 5px;
            font-size: 12px;
        """)

        # 현재 선택된 메트릭 저장
        self.current_selected_metric = metric_id

        # 후보 목록 업데이트 (메트릭 ID 기반)
        self.candidate_list.clear()
        if "TC-HW" in metric_id:
            # SASB Hardware 메트릭 - 후보 예시
            self.candidate_list.addItem("데이터 있음 - 확인 필요")
            self.candidate_list.addItem("데이터 없음")

    def on_candidate_selected(self, item):
        """후보 목록에서 항목 선택 시 - unit과 category 자동 입력"""
        # 현재 선택된 메트릭이 있는지 확인
        if not hasattr(self, 'current_selected_metric'):
            print("⚠️  먼저 왼쪽에서 메트릭을 선택해주세요!")
            return

        try:
            # metric_sid_map.json에서 unit과 category 가져오기
            metric_file = os.path.join("../new_project", "metric_sid_map.json")
            with open(metric_file, 'r', encoding='utf-8') as f:
                metrics = json.load(f)

            metric_info = metrics.get(self.current_selected_metric, {})
            unit = metric_info.get('unit', 'N/A')
            category = metric_info.get('category', 'N/A')

            # 단위 입력란에 자동 입력
            self.unit_input.setText(unit)

            # 카테고리 체크박스 자동 체크 (category가 있으면)
            if category and category != 'N/A':
                self.category_cb.setChecked(True)

            print(f"✅ 후보 선택됨: {item.text()}")
            print(f"   자동 입력 - Unit: {unit}, Category: {category}")

        except Exception as e:
            print(f"❌ 후보 선택 처리 실패: {e}")
            import traceback
            traceback.print_exc()
        
    def save_annotation(self):
        """주석 저장"""
        # 선택된 메트릭 확인
        current_item = self.metric_list.currentItem()
        if not current_item:
            print("❌ 메트릭을 선택해주세요!")
            self.save_status.setText("❌ 메트릭을 선택해주세요!")
            self.save_status.setStyleSheet("padding: 5px; background-color: #ffeaa7; color: red; border: 1px solid #fdcb6e;")
            return

        # 매핑 딕셔너리에서 메트릭 ID 가져오기
        display_text = current_item.text()
        metric_id = self.display_to_metric.get(display_text, "Unknown")
        value = self.value_input.text().strip()
        unit = self.unit_input.text().strip()
        boxes = self.image_label.get_boxes()
        
        if not value:
            print("❌ 값을 입력해주세요!")
            self.save_status.setText("❌ 값을 입력해주세요!")
            self.save_status.setStyleSheet("padding: 5px; background-color: #ffeaa7; color: red; border: 1px solid #fdcb6e;")
            return
        
        annotation = {
            'page': self.current_page,
            'value': value,
            'unit': unit,
            'category': 'quantitative',
            'complete': self.complete_cb.isChecked(),
            'bboxes': boxes,
            'cat_ok': self.category_cb.isChecked(),
            'unit_ok': self.unit_cb.isChecked(),
            'timestamp': time.time()
        }
        
        # 실제 파일로 저장
        try:
            # annotations 디렉토리 생성
            ann_dir = os.path.join("../new_project", "annotations")
            os.makedirs(ann_dir, exist_ok=True)
            
            # 메트릭 파일 경로
            safe_metric = metric_id.replace("/", "_")
            ann_file = os.path.join(ann_dir, f"{safe_metric}.json")
            
            # 기존 데이터 로드
            if os.path.exists(ann_file):
                with open(ann_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {"metric_id": metric_id, "annotations": []}
            
            # 새 주석 추가
            data["annotations"].append(annotation)
            
            # 백업 생성
            if os.path.exists(ann_file):
                backup_file = f"{ann_file}.{int(time.time())}.bak"
                shutil.copy2(ann_file, backup_file)
            
            # 파일에 저장
            with open(ann_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ 주석 저장 완료!")
            print(f"   메트릭: {metric_id}")
            print(f"   페이지: {self.current_page}")
            print(f"   값: {value} {unit}")
            print(f"   박스: {len(boxes)}개")
            print(f"   파일: {ann_file}")
            
            # 성공 상태 표시
            self.save_status.setText(f"✅ 저장됨: {value} {unit}")
            self.save_status.setStyleSheet("padding: 5px; background-color: #d1f2eb; color: green; border: 1px solid #52c41a;")
            
            # 성공 시 입력 필드 초기화
            self.value_input.clear()
            self.unit_input.clear()
            self.complete_cb.setChecked(False)
            self.category_cb.setChecked(False)
            self.unit_cb.setChecked(False)
            
        except Exception as e:
            print(f"❌ 저장 실패: {e}")
            self.save_status.setText(f"❌ 저장 실패: {str(e)[:30]}...")
            self.save_status.setStyleSheet("padding: 5px; background-color: #ffeaa7; color: red; border: 1px solid #fdcb6e;")
            import traceback
            traceback.print_exc()
        
    def clear_all_boxes(self):
        """모든 박스 지우기"""
        self.image_label.clear_boxes()
        print("모든 박스가 지워졌습니다.")
        
    def export_to_csv(self):
        """CSV 파일로 내보내기"""
        try:
            # exports 디렉토리 생성
            export_dir = os.path.join("../new_project", "exports")
            os.makedirs(export_dir, exist_ok=True)

            # 메트릭 매핑 로드
            metric_map_file = os.path.join("../new_project", "metric_sid_map.json")
            with open(metric_map_file, 'r', encoding='utf-8') as f:
                metric_map = json.load(f)

            # annotations 디렉토리에서 모든 주석 파일 로드
            ann_dir = os.path.join("../new_project", "annotations")
            all_annotations = []
            
            if os.path.exists(ann_dir):
                for filename in os.listdir(ann_dir):
                    if filename.endswith('.json') and not filename.endswith('.bak'):
                        filepath = os.path.join(ann_dir, filename)
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            all_annotations.append(data)
            
            if not all_annotations:
                print("❌ 내보낼 주석 데이터가 없습니다!")
                self.save_status.setText("❌ 내보낼 데이터 없음")
                self.save_status.setStyleSheet("padding: 5px; background-color: #ffeaa7; color: red;")
                return
            
            # 1. tsmc_5.csv - 메인 데이터 형식
            tsmc5_path = os.path.join(export_dir, "tsmc_5.csv")
            headers = ["uid", "cid", "topic", "sid", "page", "value", "unit", "complete", "x1", "y1", "x2", "y2"]
            
            with open(tsmc5_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                
                for data in all_annotations:
                    metric_id = data["metric_id"]
                    metric_info = metric_map.get(metric_id, {})
                    
                    for ann in data.get("annotations", []):
                        bboxes = ann.get("bboxes", [])
                        if not bboxes:
                            # 박스가 없는 경우 한 행 생성
                            row = [
                                "annotator",  # uid
                                "samsung",    # cid (회사명)
                                metric_info.get("topic", ""),
                                metric_info.get("sid", ""),
                                ann.get("page", ""),
                                ann.get("value", ""),
                                ann.get("unit", ""),
                                str(ann.get("complete", False)).lower(),
                                "", "", "", ""  # 빈 박스 좌표
                            ]
                            writer.writerow(row)
                        else:
                            for bbox in bboxes:
                                # bbox가 딕셔너리인지 리스트인지 확인
                                if isinstance(bbox, dict):
                                    # 딕셔너리 형태: {x1: ..., y1: ..., x2: ..., y2: ...}
                                    x1, y1, x2, y2 = bbox.get("x1", ""), bbox.get("y1", ""), bbox.get("x2", ""), bbox.get("y2", "")
                                elif isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
                                    # 리스트 형태: [x1, y1, x2, y2]
                                    x1, y1, x2, y2 = bbox[0], bbox[1], bbox[2], bbox[3]
                                else:
                                    # 알 수 없는 형태
                                    x1, y1, x2, y2 = "", "", "", ""
                                
                                row = [
                                    "annotator",  # uid
                                    "samsung",    # cid (회사명)
                                    metric_info.get("topic", ""),
                                    metric_info.get("sid", ""),
                                    ann.get("page", ""),
                                    ann.get("value", ""),
                                    ann.get("unit", ""),
                                    str(ann.get("complete", False)).lower(),
                                    x1, y1, x2, y2
                                ]
                                writer.writerow(row)
            
            # 2. full_report_agg.csv - 메트릭별 요약
            agg_path = os.path.join(export_dir, "full_report_agg.csv")
            with open(agg_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["metric", "pages", "cat_ok", "unit_ok"])
                
                for data in all_annotations:
                    pages = sorted({ann["page"] for ann in data.get("annotations", [])})
                    cat_ok = all(ann.get("cat_ok", False) for ann in data.get("annotations", []))
                    unit_ok = all(ann.get("unit_ok", False) for ann in data.get("annotations", []))
                    writer.writerow([data["metric_id"], " ".join(map(str, pages)), cat_ok, unit_ok])
            
            # 3. single_page_pairs.csv - 페이지별 상태
            pairs_path = os.path.join(export_dir, "single_page_pairs.csv")
            with open(pairs_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["metric", "page", "present", "cat_ok", "unit_ok"])
                
                for data in all_annotations:
                    pages = sorted({ann["page"] for ann in data.get("annotations", [])})
                    for page in pages:
                        page_anns = [a for a in data.get("annotations", []) if a["page"] == page]
                        writer.writerow([
                            data["metric_id"],
                            page,
                            bool(page_anns),
                            all(a.get("cat_ok", False) for a in page_anns),
                            all(a.get("unit_ok", False) for a in page_anns)
                        ])
            
            # 4. metadata.json - 메타데이터
            meta_path = os.path.join(export_dir, "metadata.json")
            metadata = {
                "company": "samsung",
                "year": 2024,
                "lang": "ko",
                "sasb_version": "1.0",
                "export_time": time.time(),
                "total_annotations": sum(len(data.get("annotations", [])) for data in all_annotations)
            }
            with open(meta_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            print("✅ CSV 내보내기 완료!")
            print(f"   📁 {export_dir}/")
            print(f"   📊 tsmc_5.csv - 메인 데이터 ({os.path.getsize(tsmc5_path)} bytes)")
            print(f"   📈 full_report_agg.csv - 메트릭 요약")
            print(f"   📄 single_page_pairs.csv - 페이지별 상태")
            print(f"   📋 metadata.json - 메타데이터")
            
            self.save_status.setText("✅ CSV 내보내기 완료!")
            self.save_status.setStyleSheet("padding: 5px; background-color: #d1f2eb; color: green;")
            
        except Exception as e:
            print(f"❌ CSV 내보내기 실패: {e}")
            self.save_status.setText(f"❌ 내보내기 실패")
            self.save_status.setStyleSheet("padding: 5px; background-color: #ffeaa7; color: red;")
            import traceback
            traceback.print_exc()

    def close_application(self):
        """애플리케이션 종료"""
        print("프로그램을 종료합니다...")
        QApplication.quit()
        
    def count_total_pages(self):
        """총 페이지 수 계산"""
        page_dir = "../new_project/pages"
        if os.path.exists(page_dir):
            png_files = [f for f in os.listdir(page_dir) if f.endswith('.png')]
            return len(png_files)
        return 0
    
    def load_current_page(self):
        """현재 페이지 로드"""
        image_path = f"../new_project/pages/{self.current_page}.png"
        if os.path.exists(image_path):
            try:
                # PIL로 이미지 로드 - 고해상도 유지
                pil_image = Image.open(image_path)
                original_size = pil_image.size
                print(f"원본 이미지 크기: {original_size}")
                
                # 더 큰 최대 크기로 설정 (해상도 대폭 향상)
                max_width, max_height = 1200, 1600  # 기존 600x800 → 1200x1600
                
                # 원본이 작으면 그대로, 크면 고품질 리샘플링
                if original_size[0] > max_width or original_size[1] > max_height:
                    pil_image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                    print(f"리사이징된 크기: {pil_image.size}")
                else:
                    print("원본 크기 그대로 사용 (더 선명함)")
                
                # PNG로 최고 품질 저장
                temp_path = f"temp_image_{self.current_page}.png"
                pil_image.save(temp_path, "PNG", compress_level=0)  # 압축 없음 = 최고 품질
                
                # QPixmap으로 로드
                pixmap = QPixmap(temp_path)
                
                # 이미지가 너무 크면 QLabel 크기 조정
                if pixmap.width() > 1000 or pixmap.height() > 800:
                    self.image_label.setMinimumSize(1000, 800)
                    
                self.image_label.setPixmap(pixmap)
                self.image_label.resize(pixmap.size())
                
                # 임시 파일 삭제
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                
                # 페이지 라벨 업데이트
                self.page_label.setText(f"페이지 {self.current_page}/{self.total_pages}")
                
                # 버튼 상태 업데이트
                self.prev_btn.setEnabled(self.current_page > 1)
                self.next_btn.setEnabled(self.current_page < self.total_pages)
                
                # 이전 페이지의 박스 지우기
                self.image_label.clear_boxes()

                # 이 페이지와 관련된 메트릭 표시 업데이트
                self.update_likely_metrics_display()

                print(f"페이지 {self.current_page} 로드 성공: {pil_image.size}")
            except Exception as e:
                print(f"페이지 {self.current_page} 로드 실패: {e}")
                self.image_label.setText(f"페이지 {self.current_page} 로드 실패")
        else:
            print(f"페이지 {self.current_page} 파일 없음: {image_path}")
            self.image_label.setText(f"페이지 {self.current_page} 파일 없음")
    
    def prev_page(self):
        """이전 페이지로 이동"""
        if self.current_page > 1:
            self.current_page -= 1
            self.load_current_page()
            print(f"이전 페이지로: {self.current_page}")
    
    def next_page(self):
        """다음 페이지로 이동"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.load_current_page()
            print(f"다음 페이지로: {self.current_page}")

    def load_image(self):
        """현재 페이지 다시 로드"""
        self.load_current_page()

def main():
    app = QApplication(sys.argv)
    
    # 한글 폰트 설정
    app.setStyleSheet("""
        QWidget {
            font-family: "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
            font-size: 12px;
        }
    """)
    
    window = ESGAnnotationApp()
    window.show()
    
    print("PyQt5 애플리케이션 시작...")
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()