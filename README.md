# 경량 ESG 주석 도구

이 프로젝트는 한 명의 주석자(annotator)가 로컬 환경에서 ESG 보고서를 효율적으로 분석할 수 있도록 고안된 순수 파이썬 기반 데스크톱 애플리케이션입니다. 별도의 서버나 복잡한 보안 구성이 필요 없으며, PDF 전처리부터 후보 발굴, 수동 검증, CSV/JSON 내보내기까지 전체 작업 흐름을 지원합니다.

## 주요 특징
- **PDF 전처리**: PyMuPDF로 페이지별 PNG와 텍스트를 생성하며, 필요 시 Tesseract OCR을 통해 이미지/표의 텍스트도 추출합니다.
- **자동 후보 발굴(Auto-Candidate Mining)**:
  - 정규식 기반 휴리스틱으로 단위(`%`, `tCO2e`, `GJ`, `m³` 등)와 숫자를 탐지하고, 지표별 동의어를 검색하여 관련 후보를 수집합니다.
  - `config.json`에 LLM 엔드포인트와 API 키를 설정하면 OpenAI 호환 API를 호출하여 추가 후보를 받을 수 있습니다.
- **Tkinter UI**: 좌측 지표 목록, 중앙 페이지 이미지(canvas)에서 박스 그리기, 우측 후보 및 값/단위 입력 패널로 구성됩니다. 키보드 단축키(화살표, `b`, `c`, `del`)를 지원하며 모든 변경 사항은 자동 저장됩니다.
- **JSON 저장소와 백업**: 지표별 JSON 파일로 주석을 저장하고, 변경 시 이전 버전을 타임스탬프 백업으로 남깁니다.
- **CSV/JSON 내보내기**: RegCom에서 요구하는 `tsmc_5.csv`, `full_report_agg.csv`, `single_page_pairs.csv`, `metadata.json` 형식을 생성합니다.

## 설치 및 실행
1. 의존성 설치
   ```bash
   pip install -r requirements.txt
   ```
2. 주석할 PDF가 들어 있는 폴더를 준비합니다.
3. 도구 실행
   ```bash
   python main.py --data_dir ./pdfs --project myproj
   ```
   - `data_dir`: 원본 PDF들이 들어 있는 디렉터리
   - `project`: 결과물이 생성될 작업 폴더 이름
4. 주석 완료 후 내보내기
   ```bash
   python export.py --project myproj --pdf ./pdfs/report.pdf --uid annotatorA --company tsmc
   ```

## 프로젝트 구조
```
myproj/
  pages/         # 페이지별 PNG와 metadata.json
  annotations/   # 자동 저장된 JSON 주석 데이터
  exports/       # CSV/JSON 내보내기 결과
  metric_sid_map.json
```

## 테스트 실행
본 저장소는 기본 기능 검증을 위한 `pytest` 기반 단위 테스트를 포함합니다.
```bash
pytest
```
테스트는 휴리스틱 후보 발굴, 저장소 동작, 내보내기 형식을 검증하여 Auto-Candidate Mining 및 데이터 관리 기능이 올바르게 작동함을 확인합니다.

## 라이선스
프로젝트는 MIT 라이선스를 따릅니다.
