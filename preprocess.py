#!/usr/bin/env python3
"""PDF 전처리 스크립트 (Tkinter 없이 실행)"""

import sys
import os
from pdf_loader import preprocess_pdf

def main():
    # 인자 파싱
    use_ocr = '--ocr' in sys.argv

    # --pdf 옵션 처리
    pdf_path = None
    output_dir = 'new_project'

    for i, arg in enumerate(sys.argv):
        if arg == '--pdf' and i + 1 < len(sys.argv):
            pdf_path = sys.argv[i + 1]
        elif arg == '--output_dir' and i + 1 < len(sys.argv):
            output_dir = sys.argv[i + 1]

    # 기존 방식 지원 (첫 번째 인자가 --로 시작하지 않으면 디렉토리로 간주)
    if pdf_path is None and len(sys.argv) > 1 and not sys.argv[1].startswith('--'):
        data_dir = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else 'new_project'

        print("=" * 60)
        print("PDF 전처리 시작")
        print("=" * 60)
        print(f"입력 디렉토리: {data_dir}")
        print(f"프로젝트명: {output_dir}")
        print(f"OCR 사용: {'예' if use_ocr else '아니오'}")
        print("=" * 60)

        # PDF 파일 목록 확인
        if not os.path.exists(data_dir):
            print(f"❌ 오류: {data_dir} 디렉토리가 없습니다.")
            return 1

        pdf_files = [f for f in os.listdir(data_dir) if f.endswith('.pdf')]
        if not pdf_files:
            print(f"❌ 오류: {data_dir}에 PDF 파일이 없습니다.")
            return 1

        print(f"\n발견된 PDF 파일 ({len(pdf_files)}개):")
        for i, pdf in enumerate(pdf_files, 1):
            print(f"  {i}. {pdf}")
        print()

        # 첫 번째 PDF 파일 선택
        pdf_path = os.path.join(data_dir, pdf_files[0])

    # PDF 경로가 지정되지 않았으면 기본값 사용
    if pdf_path is None:
        data_dir = './pdfs'
        if not os.path.exists(data_dir):
            print(f"❌ 오류: {data_dir} 디렉토리가 없습니다.")
            return 1
        pdf_files = [f for f in os.listdir(data_dir) if f.endswith('.pdf')]
        if not pdf_files:
            print(f"❌ 오류: {data_dir}에 PDF 파일이 없습니다.")
            return 1
        pdf_path = os.path.join(data_dir, pdf_files[0])

    # PDF 파일 존재 확인
    if not os.path.exists(pdf_path):
        print(f"❌ 오류: {pdf_path} 파일이 없습니다.")
        return 1

    print("=" * 60)
    print("PDF 전처리 시작")
    print("=" * 60)
    print(f"입력 PDF: {pdf_path}")
    print(f"출력 디렉토리: {output_dir}")
    print(f"OCR 사용: {'예' if use_ocr else '아니오'}")
    print("=" * 60)
    print(f"\n처리 중: {os.path.basename(pdf_path)}\n")

    # PDF 전처리 실행
    try:
        preprocess_pdf(pdf_path, output_dir, ocr=use_ocr)

        print("\n" + "=" * 60)
        print("✅ PDF 전처리 완료!")
        print("=" * 60)
        print(f"결과 위치: {output_dir}/pages/")
        print(f"- 페이지 이미지: {output_dir}/pages/*.png")
        print(f"- 메타데이터: {output_dir}/pages/metadata.json")
        print("\n다음 단계:")
        print("  1. jupyter notebook candidate_miner/heuristic_analysis.ipynb")
        print("  2. cd esg_test && python pyqt5_gui.py")
        return 0
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
