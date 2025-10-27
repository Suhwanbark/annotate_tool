# ESG Report Annotation Tool

SASB 메트릭 기반 ESG 보고서 주석 도구

---

## 빠른 시작 (사용자용)

레포지토리를 클론한 후 바로 사용하는 방법입니다.

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. GUI 실행
```bash
cd esg_test
python pyqt5_gui.py --project ../projects/hyundai_2024
```

**다른 프로젝트 실행:**
```bash
# 삼성전자
python pyqt5_gui.py --project ../projects/samsung_2024

# SK하이닉스
python pyqt5_gui.py --project ../projects/sk_hynix_2024
```

### 3. 주석 작업
- **왼쪽**: 메트릭 목록에서 선택
- **중앙**: 페이지 이동 + 마우스 드래그로 bounding box 그리기
- **오른쪽**: 값/단위 입력 후 "💾 주석 저장" 클릭

### 4. 데이터 내보내기
오른쪽 패널 하단의 "📊 CSV 내보내기" 버튼 클릭
- 결과 위치: `projects/{프로젝트명}/exports/`

---

## 개발자 매뉴얼: 새 프로젝트 추가

새로운 회사의 ESG 보고서를 추가하는 방법입니다.

### Step 1: PDF 전처리

PDF를 페이지별 PNG 이미지로 변환합니다.

```bash
python preprocess.py --pdf "./pdfs/회사명_2024.pdf" --output_dir projects/회사명_2024
```

**출력:**
- `projects/회사명_2024/pages/*.png` - 페이지 이미지
- `projects/회사명_2024/pages/metadata.json` - 텍스트 메타데이터

**OCR 사용 (선택):**
```bash
python preprocess.py --pdf "./pdfs/회사명_2024.pdf" --output_dir projects/회사명_2024 --ocr
```

---

### Step 2: 메트릭 정의 및 키워드 작성 (수동)

프로젝트 폴더에 두 개의 파일을 **직접 작성**합니다.

#### 2-1. `metric_sid_map.json` 작성

SASB 메트릭 정의 파일입니다.

```json
{
  "TR-AU-250a.1": {
    "topic": "Product Safety",
    "sid": "Percentage of vehicle models rated by NCAP with an overall 5-star safety rating",
    "unit": "Percentage (%)",
    "category": "Quantitative"
  },
  "TR-AU-410a.2": {
    "topic": "Fuel Economy & Use-phase Emissions",
    "sid": "Number of zero emission vehicles (ZEV) sold",
    "unit": "Number",
    "category": "Quantitative"
  }
}
```

**참고:** 기존 프로젝트의 파일을 복사하여 수정하세요.
```bash
cp projects/samsung_2024/metric_sid_map.json projects/회사명_2024/
```

#### 2-2. `metric_keywords.py` 작성

메트릭별 검색 키워드를 정의합니다 (한국어 + 영어).

```python
#!/usr/bin/env python3
"""메트릭별 키워드 매핑"""

METRIC_KEYWORDS = {
    "TR-AU-250a.1": [
        "NCAP", "안전등급", "안전성", "5성", "충돌테스트",
        "safety rating", "5-star", "crash test",
    ],
    "TR-AU-410a.2": [
        "전기차", "하이브리드", "ZEV", "EV", "친환경차",
        "electric vehicle", "zero emission", "plug-in",
    ],
}
```

**참고:** 기존 프로젝트의 파일을 복사하여 수정하세요.
```bash
cp projects/samsung_2024/metric_keywords.py projects/회사명_2024/
```

---

### Step 3: 후보 페이지 필터링 (Jupyter Notebook)

키워드를 기반으로 각 메트릭과 관련된 페이지를 자동으로 추출합니다.

```bash
jupyter notebook candidate_miner/heuristic_analysis.ipynb
```

**노트북에서 수정:**
1. Cell 2의 `PROJECT_DIR` 변경:
   ```python
   PROJECT_DIR = Path('../projects/회사명_2024')
   ```
2. 모든 셀 실행 (Cell → Run All)

**출력:**
- `projects/회사명_2024/metric_page_mapping.json` - 메트릭별 관련 페이지 매핑

---

### Step 4: GUI 실행

```bash
cd esg_test
python pyqt5_gui.py --project ../projects/회사명_2024
```

이제 주석 작업을 시작할 수 있습니다!

---

## 프로젝트 구조

```
annotate/
├── esg_test/
│   └── pyqt5_gui.py           # ⭐ GUI 메인 애플리케이션
├── candidate_miner/
│   └── heuristic_analysis.ipynb  # ⭐ 페이지 필터링 노트북
├── preprocess.py              # ⭐ PDF → PNG 변환
├── projects/                  # 회사별 프로젝트 폴더
│   ├── samsung_2024/
│   │   ├── metric_sid_map.json    # 메트릭 정의
│   │   ├── metric_keywords.py     # 키워드 매핑
│   │   ├── metric_page_mapping.json  # 필터링 결과
│   │   ├── pages/                 # PNG 이미지
│   │   ├── annotations/           # 주석 JSON
│   │   └── exports/               # CSV 결과
│   ├── sk_hynix_2024/
│   └── hyundai_2024/
└── pdfs/                      # 입력 PDF 파일
```

---

## 내보내기 형식

CSV 내보내기 버튼 클릭 시 생성되는 파일:

- `tsmc_5.csv` - 메인 데이터 (uid, cid, topic, sid, page, value, unit, ambiguous, x1, y1, x2, y2)
- `full_report_agg.csv` - 메트릭별 요약 (metric, pages, cat_ok, ambiguous)
- `single_page_pairs.csv` - 페이지별 상태 (metric, page, present, cat_ok, ambiguous)
- `metadata.json` - 메타데이터 (company, year, export_time, total_annotations)

---

## 라이선스

MIT License
