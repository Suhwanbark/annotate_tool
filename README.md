# ESG Report Annotation Tool

**SASB Hardware 메트릭 기반 ESG 보고서 주석 도구**

이 도구는 ESG(Environmental, Social, Governance) 보고서에서 SASB Hardware 메트릭 데이터를 효율적으로 추출하고 주석을 다는 데스크톱 애플리케이션입니다. 순수 Python으로 작성되었으며, 서버나 복잡한 설정 없이 로컬에서 안전하게 사용할 수 있습니다.

## 📋 목차

- [주요 기능](#주요-기능)
- [설치 방법](#설치-방법)
- [빠른 시작](#빠른-시작)
- [상세 사용 가이드](#상세-사용-가이드)
- [프로젝트 구조](#프로젝트-구조)
- [메트릭 정보](#메트릭-정보)
- [내보내기 형식](#내보내기-형식)
- [개발자 가이드](#개발자-가이드)

---

## 🎯 주요 기능

### 1. **PDF 전처리 및 시각화**
- PyMuPDF를 사용한 고품질 페이지별 PNG 변환
- 옵션: Tesseract OCR을 통한 이미지/표 텍스트 추출
- 고해상도 이미지 뷰어로 선명한 문서 확인

### 2. **지능형 후보 마이닝**
- **휴리스틱 방식**: 키워드 기반 페이지 필터링 (영어 + 한국어 365개 키워드)
- **LLM 방식** (선택): API 호출을 통한 정밀 후보 추출
- 페이지별 관련 메트릭 자동 추천

### 3. **직관적인 GUI (PyQt5)**
- **3패널 구조**: 메트릭 목록 | 페이지 뷰어 | 주석 입력
- 마우스 드래그로 bounding box 그리기
- 자동 완성: 메트릭 선택 시 category와 unit 자동 입력
- 메트릭별 상세 정보 표시 (Topic, SID, Category, Unit)

### 4. **데이터 관리**
- 메트릭별 JSON 자동 저장 (타임스탬프 백업)
- CSV/JSON 다중 형식 내보내기
- RegCom 요구사항 준수 포맷

---

## 🚀 설치 방법

### 필수 요구사항
- Python 3.9 이상
- macOS, Windows, Linux 지원

### 1. 레포지토리 클론
```bash
git clone https://github.com/your-username/esg-annotation-tool.git
cd esg-annotation-tool
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

**필수 패키지:**
- `PyMuPDF` - PDF 처리
- `Pillow` - 이미지 처리
- `PyQt5` - GUI 프레임워크
- `pandas`, `matplotlib`, `seaborn` - 데이터 분석
- `jupyter`, `ipykernel` - Jupyter 노트북

**선택 패키지:**
- `pytesseract` - OCR (이미지/표 텍스트 추출)
- `requests` - LLM API 호출

### 3. OCR 설치 (선택)
```bash
# macOS
brew install tesseract tesseract-lang

# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-kor

# Windows
# https://github.com/UB-Mannheim/tesseract/wiki 에서 설치
```

---

## ⚡ 빠른 시작

### 1단계: PDF 전처리
```bash
python main.py --data_dir ./pdfs --project myproj
```

### 2단계: 후보 마이닝
```bash
jupyter notebook candidate_miner/heuristic_analysis.ipynb
# 노트북에서 모든 셀 실행
```

### 3단계: GUI 실행
```bash
cd esg_test
python pyqt5_gui.py
```

### 4단계: 데이터 내보내기
GUI에서 **📊 CSV 내보내기** 버튼 클릭

---

## 📖 상세 사용 가이드

### 단계 1: PDF 전처리

PDF 파일을 페이지별 PNG 이미지로 변환합니다.

```bash
# 기본 사용 (텍스트만 추출)
python main.py --data_dir ./pdfs --project myproj

# OCR 사용 (이미지/표 텍스트 추출)
python main.py --data_dir ./pdfs --project myproj --ocr
```

**출력:**
- `myproj/pages/*.png` - 페이지별 이미지
- `myproj/pages/metadata.json` - 페이지 메타데이터

### 단계 2: 후보 마이닝

키워드 기반으로 각 메트릭과 관련된 페이지를 찾습니다.

```bash
jupyter notebook candidate_miner/heuristic_analysis.ipynb
```

**노트북에서:**
1. 프로젝트 경로 설정: `project_dir = "../myproj"`
2. 모든 셀 실행 (`Shift + Enter`)
3. `metric_page_mapping.json` 생성 확인

**출력:**
- `myproj/metric_page_mapping.json` - 메트릭별 관련 페이지 목록

### 단계 3: GUI 주석 작업

```bash
cd esg_test
python pyqt5_gui.py
```

#### GUI 사용법

**왼쪽 패널 - 메트릭 목록**
- 메트릭 클릭하여 선택
- 표시 정보: Topic, SID, Category, Unit
- 선택된 메트릭이 녹색으로 하이라이트

**중앙 패널 - 페이지 뷰어**
- ◀/▶ 버튼으로 페이지 이동
- 노란색 박스: 현재 페이지의 관련 메트릭 자동 추천 (스크롤 가능)
- 마우스 드래그로 데이터 영역에 bounding box 그리기

**오른쪽 패널 - 주석 입력**
1. 후보 목록에서 항목 선택 → Unit/Category 자동 입력
2. **값**: 추출한 데이터 값 입력
3. **단위**: 자동 입력 (수정 가능)
4. 체크박스: 완료, 카테고리 OK, 단위 OK
5. **💾 주석 저장** 버튼 클릭

**자동 저장:**
- `myproj/annotations/{metric_id}.json`
- 타임스탬프 백업 (`.bak`)

### 단계 4: 데이터 내보내기

**GUI에서:**
- **📊 CSV 내보내기** 버튼 클릭

**CLI에서:**
```bash
python -m annotation.export \
  --project myproj \
  --pdf ./pdfs/samsung_2024.pdf \
  --uid annotatorA \
  --company samsung
```

**출력 (`myproj/exports/`):**
- `tsmc_5.csv` - 메인 데이터
- `full_report_agg.csv` - 메트릭 요약
- `single_page_pairs.csv` - 페이지별 상태
- `metadata.json` - 메타데이터

---

## 📁 프로젝트 구조

```
esg-annotation-tool/
├── README.md                   # 📖 이 문서
├── requirements.txt            # 의존성 목록
├── CLAUDE.md                   # Claude Code 가이드
├── .gitignore                  # Git 제외 파일
│
├── main.py                     # PDF 전처리 진입점
├── pdf_loader.py               # PDF → PNG 변환
├── ui.py                       # Tkinter UI (legacy)
├── utils.py                    # 유틸리티 함수
│
├── esg_test/
│   └── pyqt5_gui.py           # ⭐ PyQt5 메인 GUI
│
├── annotation/
│   ├── store.py               # JSON 저장
│   └── export.py              # CSV/JSON 내보내기
│
├── candidate_miner/
│   ├── heuristics.py          # 휴리스틱 마이닝
│   ├── llm_miner.py           # LLM 마이닝 (선택)
│   ├── prompts.py             # LLM 프롬프트
│   └── heuristic_analysis.ipynb  # ⭐ 페이지 필터링 노트북
│
├── myproj/                    # 작업 디렉토리 (예시)
│   ├── metric_sid_map.json    # SASB 메트릭 정의
│   ├── metric_keywords.py     # 키워드 매핑 (365개)
│   ├── metric_page_mapping.json  # 메트릭-페이지 매핑
│   ├── pages/                 # PDF 페이지 PNG
│   ├── annotations/           # 주석 JSON
│   └── exports/               # CSV 결과
│
├── config/
│   └── config.example.json    # LLM API 설정 템플릿
│
├── tests/                     # pytest 테스트
│   ├── test_candidate_miner.py
│   ├── test_export.py
│   ├── test_store.py
│   └── test_utils.py
│
└── pdfs/                      # 입력 PDF 디렉토리
```

---

## 📊 메트릭 정보

### SASB Hardware 메트릭 (9개)

| 메트릭 ID | Topic | Category | Unit |
|----------|-------|----------|------|
| TC-HW-230a.1 | Product Security | Discussion and Analysis | n/a |
| TC-HW-330a.1 | Employee Diversity & Inclusion | Quantitative | Percentage (%) |
| TC-HW-410a.1 | Product Lifecycle Management | Quantitative | Percentage (%) |
| TC-HW-410a.2 | Product Lifecycle Management | Quantitative | Percentage (%) |
| TC-HW-410a.3 | Product Lifecycle Management | Quantitative | Percentage (%) |
| TC-HW-410a.4 | Product Lifecycle Management | Quantitative | Metric tonnes (t), % |
| TC-HW-430a.1 | Supply Chain Management | Quantitative | Percentage (%) |
| TC-HW-430a.2 | Supply Chain Management | Quantitative | Rate |
| TC-HW-440a.1 | Materials Sourcing | Discussion and Analysis | n/a |

### 키워드 매핑
- **총 365개** (영어 + 한국어)
- 파일: `myproj/metric_keywords.py`
- 예시:
  - TC-HW-230a.1: "security", "cyber", "보안", "데이터 보안"
  - TC-HW-410a.4: "e-waste", "recycling", "전자폐기물", "재활용"

---

## 📤 내보내기 형식

### 1. tsmc_5.csv (메인 데이터)
```csv
uid,cid,topic,sid,page,value,unit,complete,x1,y1,x2,y2
annotatorA,samsung,Product Security,Description of...,1,Yes,n/a,true,100,200,300,400
```

### 2. full_report_agg.csv (메트릭 요약)
```csv
metric,pages,cat_ok,unit_ok
TC-HW-230a.1,1 2 3,true,true
```

### 3. single_page_pairs.csv (페이지 상태)
```csv
metric,page,present,cat_ok,unit_ok
TC-HW-230a.1,1,true,true,true
```

### 4. metadata.json
```json
{
  "company": "samsung",
  "year": 2024,
  "lang": "ko",
  "sasb_version": "1.0",
  "export_time": 1697200000.0,
  "total_annotations": 15
}
```

---

## 🛠️ 개발자 가이드

### 테스트 실행

```bash
# 전체 테스트
pytest

# 특정 테스트
pytest tests/test_candidate_miner.py

# 문법 체크
python -m py_compile $(git ls-files '*.py')
```

### LLM 마이닝 (선택)

1. config 파일 생성:
```bash
cp config/config.example.json config/config.json
```

2. API 정보 입력:
```json
{
  "llm_base_url": "https://api.openai.com/v1",
  "llm_model": "gpt-4",
  "api_key": "sk-..."
}
```

3. 사용:
```python
from candidate_miner.llm_miner import mine_with_llm
candidates = mine_with_llm(page_text, metric_id, config)
```

### 새 메트릭 추가

1. `myproj/metric_sid_map.json`에 정의 추가
2. `myproj/metric_keywords.py`에 키워드 추가
3. `heuristic_analysis.ipynb` 재실행

---

## 🤝 기여하기

1. Fork this repository
2. Create feature branch: `git checkout -b feature/name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature/name`
5. Open Pull Request

**가이드라인:**
- pytest 테스트 추가
- 문법 체크 통과
- CLAUDE.md 참고

---

## 📝 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능

---

## 📧 문의

- Issues: GitHub Issues
- Docs: CLAUDE.md

---

## 🙏 감사

- SASB Standards Board
- PyMuPDF, PyQt5, Tesseract 커뮤니티
