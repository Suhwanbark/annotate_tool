"""
SASB Hardware 메트릭별 키워드 매핑

각 메트릭과 관련된 영문 + 한글 키워드를 정의합니다.
페이지 필터링 및 후보 마이닝에 사용됩니다.
"""

# 메트릭별 키워드 매핑 (영어 + 한국어)
METRIC_KEYWORDS = {
    "TC-HW-230a.1": [
        # Product Security (영어)
        "security", "data security", "cyber", "cybersecurity",
        "privacy", "data privacy", "data protection",
        "breach", "data breach", "vulnerability", "vulnerabilities",
        "encryption", "authentication", "access control",
        "incident", "security incident", "threat",
        "ISO 27001", "SOC 2", "GDPR", "compliance",
        "penetration test", "security audit", "risk assessment",
        # Product Security (한국어)
        "보안", "데이터 보안", "정보보안", "사이버",
        "개인정보", "프라이버시", "정보 보호",
        "침해", "유출", "취약점", "취약성",
        "암호화", "인증", "접근 제어", "접근제어",
        "사고", "보안 사고", "위협",
        "컴플라이언스", "규제 준수",
        "침투 테스트", "보안 점검", "보안 감사", "위험 평가"
    ],

    "TC-HW-330a.1": [
        # Employee Diversity & Inclusion (영어)
        "diversity", "inclusion", "gender", "female", "male",
        "representation", "workforce", "employee",
        "management", "executive", "technical", "non-executive",
        "women", "minority", "underrepresented",
        "equal opportunity", "EEO", "affirmative action",
        "demographic", "composition", "breakdown",
        # Employee Diversity & Inclusion (한국어)
        "다양성", "포용성", "포용", "포괄성",
        "성별", "여성", "남성", "젠더",
        "대표성", "구성비", "비율",
        "임직원", "직원", "인력", "구성원",
        "경영진", "임원", "관리자", "기술직", "비관리직",
        "소수자", "소수집단", "취약계층",
        "평등", "기회 균등", "균등", "차별 금지"
    ],

    "TC-HW-410a.1": [
        # Product Lifecycle Management - IEC 62474 substances (영어)
        "IEC 62474", "declarable substance", "hazardous substance",
        "restricted substance", "material declaration",
        "RoHS", "REACH", "conflict minerals",
        "lead", "mercury", "cadmium", "hexavalent chromium",
        "substance of concern", "chemical", "material composition",
        "product content", "compliance",
        # Product Lifecycle Management - IEC 62474 substances (한국어)
        "신고 물질", "유해 물질", "유해물질",
        "제한 물질", "제한물질", "규제 물질",
        "물질 신고", "성분 신고",
        "납", "수은", "카드뮴", "6가 크롬",
        "우려 물질", "화학물질", "소재 구성",
        "제품 함유", "함유 물질"
    ],

    "TC-HW-410a.2": [
        # Product Lifecycle Management - EPEAT (영어)
        "EPEAT", "electronic product environmental assessment",
        "eco-label", "environmental certification",
        "green product", "sustainable product",
        "registration", "certified product",
        "gold", "silver", "bronze",
        "environmental performance", "eco-design",
        # Product Lifecycle Management - EPEAT (한국어)
        "환경 인증", "친환경 인증",
        "에코라벨", "환경 라벨", "환경마크",
        "친환경 제품", "녹색 제품",
        "지속가능", "지속 가능", "지속가능한",
        "등록", "인증 제품",
        "골드", "실버", "브론즈",
        "환경 성능", "환경성능", "친환경 설계"
    ],

    "TC-HW-410a.3": [
        # Product Lifecycle Management - Energy efficiency (영어)
        "energy efficiency", "energy star", "energy consumption",
        "power consumption", "efficient", "efficiency certification",
        "energy rating", "energy performance",
        "low power", "power saving", "standby power",
        "80 plus", "efficiency standard",
        "watt", "kwh", "energy use",
        # Product Lifecycle Management - Energy efficiency (한국어)
        "에너지 효율", "에너지효율", "고효율",
        "에너지 소비", "소비 전력", "전력 소비",
        "에너지 인증", "효율 인증",
        "에너지 등급", "효율 등급",
        "저전력", "절전", "대기전력",
        "와트", "전력", "소비량"
    ],

    "TC-HW-410a.4": [
        # Product Lifecycle Management - E-waste (영어)
        "e-waste", "electronic waste", "WEEE",
        "end-of-life", "EOL", "product take-back",
        "recycling", "recycled", "recovery", "recovered",
        "circular economy", "refurbishment", "reuse",
        "waste management", "disposal",
        "metric ton", "tonne", "kg", "kilogram",
        "recycling rate", "collection",
        # Product Lifecycle Management - E-waste (한국어)
        "전자폐기물", "전자 폐기물", "폐전자",
        "폐기물", "폐기", "사용 후",
        "제품 회수", "회수", "수거",
        "재활용", "재생", "회수율",
        "순환경제", "순환 경제", "재사용", "재제조",
        "폐기물 관리", "처리",
        "톤", "킬로그램", "중량",
        "재활용률", "재활용율"
    ],

    "TC-HW-430a.1": [
        # Supply Chain Management - RBA audit (영어)
        "RBA", "responsible business alliance",
        "VAP", "validated audit process",
        "supplier", "tier 1", "tier 1 supplier",
        "audit", "audited", "facility", "facilities",
        "high-risk", "high risk",
        "supply chain", "supplier assessment",
        "third-party audit", "independent audit",
        "compliance audit",
        # Supply Chain Management - RBA audit (한국어)
        "협력사", "공급업체", "공급사", "납품업체",
        "1차 협력사", "티어1", "1차 공급사",
        "감사", "점검", "평가", "심사",
        "사업장", "공장", "시설",
        "고위험", "고 위험", "위험",
        "공급망", "공급체인", "협력망",
        "제3자 감사", "독립 감사",
        "준수 감사", "컴플라이언스"
    ],

    "TC-HW-430a.2": [
        # Supply Chain Management - Non-conformance (영어)
        "non-conformance", "nonconformance", "non conformance",
        "corrective action", "CAPA", "remediation",
        "priority non-conformance", "major non-conformance",
        "minor non-conformance", "finding",
        "supplier performance", "audit finding",
        "improvement", "action plan",
        "conformance rate", "compliance rate",
        # Supply Chain Management - Non-conformance (한국어)
        "부적합", "부적합사항", "미준수",
        "시정조치", "시정 조치", "개선 조치",
        "개선", "조치", "시정",
        "우선 부적합", "중대 부적합", "경미한 부적합",
        "발견사항", "지적사항",
        "협력사 성과", "공급사 성과",
        "감사 결과", "점검 결과",
        "개선 계획", "실행 계획",
        "준수율", "적합률"
    ],

    "TC-HW-440a.1": [
        # Materials Sourcing - Critical materials (영어)
        "critical material", "strategic material",
        "rare earth", "cobalt", "lithium", "tantalum",
        "conflict mineral", "3TG", "tin", "tungsten", "gold",
        "supply risk", "material risk", "sourcing risk",
        "supply chain transparency", "traceability",
        "responsible sourcing", "ethical sourcing",
        "material scarcity", "resource availability",
        "due diligence", "supplier audit",
        # Materials Sourcing - Critical materials (한국어)
        "핵심 소재", "핵심 자원", "중요 소재",
        "전략 소재", "전략 자원",
        "희토류", "희소금속", "코발트", "리튬", "탄탈룸",
        "분쟁광물", "분쟁 광물", "주석", "텅스텐",
        "공급 리스크", "공급 위험", "소재 위험",
        "조달 위험", "조달 리스크",
        "공급망 투명성", "추적가능성", "추적성",
        "책임 있는 조달", "책임조달", "윤리적 조달",
        "소재 부족", "자원 가용성",
        "실사", "공급사 감사"
    ]
}


def get_keywords(metric_id):
    """특정 메트릭의 키워드 리스트를 반환합니다."""
    return METRIC_KEYWORDS.get(metric_id, [])


def get_all_keywords():
    """모든 메트릭의 키워드를 반환합니다."""
    all_keywords = set()
    for keywords in METRIC_KEYWORDS.values():
        all_keywords.update(keywords)
    return sorted(list(all_keywords))


if __name__ == "__main__":
    print("=" * 60)
    print("SASB Hardware 메트릭별 키워드 매핑")
    print("=" * 60)

    for metric_id, keywords in METRIC_KEYWORDS.items():
        print(f"\n{metric_id}: {len(keywords)}개 키워드")
        print(f"  첫 8개: {', '.join(keywords[:8])}")

    print("\n" + "=" * 60)
    print(f"전체 고유 키워드 수: {len(get_all_keywords())}")
    print("=" * 60)
