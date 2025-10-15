"""
SASB Semiconductors 메트릭별 키워드 매핑

각 메트릭과 관련된 영문 + 한글 키워드를 정의합니다.
페이지 필터링 및 후보 마이닝에 사용됩니다.
"""

# 메트릭별 키워드 매핑 (영어 + 한국어)
METRIC_KEYWORDS = {
    "TC-SC-110a.1": [
        # Greenhouse Gas Emissions - Scope 1 & PFCs (영어)
        "scope 1", "scope 1 emission", "direct emission",
        "GHG", "greenhouse gas", "carbon emission", "CO2", "CO2e",
        "PFC", "perfluorinated compound", "perfluorocarbon",
        "CF4", "C2F6", "NF3", "SF6", "CHF3", "C3F8",
        "fluorinated gas", "F-gas", "process gas",
        "semiconductor manufacturing emission",
        "metric ton", "tonne", "CO2 equivalent",
        # Greenhouse Gas Emissions - Scope 1 & PFCs (한국어)
        "스코프 1", "스코프1", "직접 배출", "직접배출",
        "온실가스", "온실 가스", "탄소 배출", "이산화탄소",
        "불화가스", "과불화화합물", "퍼플루오로",
        "공정가스", "반도체 공정", "제조 배출",
        "배출량", "총 배출량", "글로벌 배출",
        "톤", "메트릭톤", "이산화탄소 환산"
    ],

    "TC-SC-110a.2": [
        # Greenhouse Gas Emissions - Strategy (영어)
        "emission reduction", "reduction target", "emission target",
        "climate strategy", "carbon strategy", "decarbonization",
        "net zero", "carbon neutral", "climate goal",
        "long-term target", "short-term target", "2030", "2050",
        "mitigation", "abatement", "reduction plan",
        "performance", "progress", "achievement",
        "scope 1 management", "emission management",
        # Greenhouse Gas Emissions - Strategy (한국어)
        "배출 감축", "감축 목표", "탄소 감축",
        "기후 전략", "탄소 전략", "탈탄소",
        "탄소중립", "넷제로", "넷 제로", "기후 목표",
        "장기 목표", "단기 목표", "중장기",
        "저감", "완화", "감축 계획", "실행 계획",
        "성과", "진행", "달성", "이행",
        "배출 관리", "온실가스 관리"
    ],

    "TC-SC-130a.1": [
        # Energy Management in Manufacturing (영어)
        "energy consumption", "total energy", "energy use",
        "grid electricity", "electricity consumption", "power consumption",
        "renewable", "renewable energy", "solar", "wind",
        "clean energy", "green energy", "RE100",
        "energy source", "power source", "electricity source",
        "gigajoule", "GJ", "MWh", "kWh", "terajoule",
        "manufacturing energy", "facility energy",
        "percentage renewable", "renewable ratio",
        # Energy Management in Manufacturing (한국어)
        "에너지 소비", "총 에너지", "에너지 사용",
        "전력 소비", "전기 소비", "전력 사용량",
        "재생에너지", "재생 에너지", "신재생",
        "태양광", "풍력", "청정에너지", "녹색에너지",
        "에너지원", "전력원", "전기원",
        "기가줄", "메가와트시", "킬로와트시",
        "제조 에너지", "사업장 에너지", "공장 에너지",
        "재생에너지 비율", "재생에너지 비중"
    ],

    "TC-SC-140a.1": [
        # Water Management (영어)
        "water", "water withdrawal", "water consumption",
        "water use", "water intake", "freshwater",
        "water stress", "water risk", "water scarcity",
        "high baseline water stress", "extremely high water stress",
        "water-stressed region", "water-scarce area",
        "cubic meter", "m3", "thousand cubic meter",
        "wastewater", "water discharge", "water recycling",
        "water management", "water stewardship",
        # Water Management (한국어)
        "물", "용수", "수자원",
        "취수", "취수량", "물 사용", "용수 사용",
        "담수", "상수", "공업용수",
        "물 스트레스", "수자원 부족", "물 부족",
        "고위험 지역", "물 부족 지역", "수자원 위험",
        "입방미터", "천 입방미터",
        "폐수", "방류", "재이용", "재활용",
        "용수 관리", "수자원 관리", "물 관리"
    ],

    "TC-SC-150a.1": [
        # Waste Management (영어)
        "hazardous waste", "industrial waste", "waste generation",
        "waste disposal", "waste treatment", "waste management",
        "recycling", "recycled", "recycle rate", "recovery",
        "waste reduction", "waste minimization",
        "chemical waste", "toxic waste", "special waste",
        "metric ton", "tonne", "kg", "kilogram",
        "percentage recycled", "recycling rate",
        "waste-to-resource", "circular economy",
        # Waste Management (한국어)
        "유해폐기물", "유해 폐기물", "산업폐기물",
        "폐기물", "폐기물 발생", "폐기물 배출",
        "폐기물 처리", "폐기물 관리", "처리",
        "재활용", "재활용률", "재활용율", "재생",
        "폐기물 감축", "폐기물 저감",
        "화학폐기물", "독성폐기물", "지정폐기물",
        "톤", "킬로그램", "중량",
        "재활용 비율", "재활용 비중",
        "자원순환", "순환경제"
    ],

    "TC-SC-320a.1": [
        # Workforce Health & Safety - Assessment (영어)
        "health hazard", "human health", "occupational health",
        "workplace safety", "worker safety", "employee safety",
        "exposure", "chemical exposure", "hazardous exposure",
        "industrial hygiene", "occupational hygiene",
        "monitoring", "assessment", "risk assessment",
        "health surveillance", "medical surveillance",
        "personal protective equipment", "PPE",
        "safety program", "health program",
        "ventilation", "air quality", "environmental monitoring",
        # Workforce Health & Safety - Assessment (한국어)
        "건강 위해", "건강 유해", "직업 건강",
        "작업장 안전", "근로자 안전", "직원 안전",
        "노출", "화학물질 노출", "유해물질 노출",
        "산업위생", "작업환경", "작업장 위생",
        "모니터링", "평가", "위험 평가", "위험성 평가",
        "건강 감시", "건강검진", "특수검진",
        "보호구", "개인보호장비", "안전장비",
        "안전 프로그램", "보건 프로그램",
        "환기", "공기질", "환경 모니터링"
    ],

    "TC-SC-320a.2": [
        # Workforce Health & Safety - Legal proceedings (영어)
        "monetary loss", "legal proceeding", "litigation",
        "fine", "penalty", "settlement", "damages",
        "health and safety violation", "OSHA", "violation",
        "regulatory action", "enforcement action",
        "lawsuit", "legal action", "claim",
        "compensation", "liability", "financial impact",
        # Workforce Health & Safety - Legal proceedings (한국어)
        "금전적 손실", "금전 손실", "벌금",
        "법적 절차", "소송", "법적 조치",
        "과태료", "과징금", "합의금", "손해배상",
        "안전보건 위반", "산업안전 위반", "위반",
        "규제 조치", "행정 조치", "처분",
        "법적 소송", "법적 청구", "배상 청구",
        "보상", "배상", "책임", "재무 영향"
    ],

    "TC-SC-330a.1": [
        # Recruiting & Managing a Global & Skilled Workforce (영어)
        "work visa", "foreign worker", "international employee",
        "visa requirement", "immigration", "work permit",
        "H-1B", "skilled worker visa", "employment visa",
        "expatriate", "expat", "migrant worker",
        "workforce composition", "employee composition",
        "percentage", "proportion", "ratio",
        "talent", "skilled workforce", "technical talent",
        # Recruiting & Managing a Global & Skilled Workforce (한국어)
        "취업비자", "취업 비자", "비자",
        "외국인 근로자", "외국인 인력", "해외 인력",
        "비자 요구", "이민", "취업 허가", "근로 허가",
        "숙련 인력", "전문 인력",
        "국외 근무", "해외 파견", "주재원",
        "인력 구성", "직원 구성", "임직원 구성",
        "비율", "비중", "퍼센트",
        "인재", "숙련 인력", "기술 인력", "전문인력"
    ],

    "TC-SC-410a.1": [
        # Product Lifecycle Management - IEC 62474 substances (영어)
        "IEC 62474", "declarable substance", "hazardous substance",
        "restricted substance", "material declaration",
        "RoHS", "REACH", "conflict minerals",
        "lead", "mercury", "cadmium", "hexavalent chromium",
        "substance of concern", "chemical", "material composition",
        "product content", "compliance", "substance reporting",
        "percentage", "revenue", "products",
        # Product Lifecycle Management - IEC 62474 substances (한국어)
        "신고 물질", "유해 물질", "유해물질",
        "제한 물질", "제한물질", "규제 물질",
        "물질 신고", "성분 신고", "물질 보고",
        "납", "수은", "카드뮴", "6가 크롬",
        "우려 물질", "화학물질", "소재 구성",
        "제품 함유", "함유 물질", "제품 성분",
        "준수", "컴플라이언스",
        "비율", "매출", "제품"
    ],

    "TC-SC-410a.2": [
        # Product Lifecycle Management - Processor energy efficiency (영어)
        "processor", "chip", "semiconductor",
        "energy efficiency", "power efficiency", "performance per watt",
        "server", "desktop", "laptop",
        "system-level", "system level efficiency",
        "energy performance", "power consumption",
        "computational efficiency", "processing efficiency",
        "benchmark", "performance metric",
        "SPEC", "TDP", "thermal design power",
        # Product Lifecycle Management - Processor energy efficiency (한국어)
        "프로세서", "칩", "반도체", "처리장치",
        "에너지 효율", "전력 효율", "성능 대 전력",
        "서버", "데스크톱", "노트북", "랩톱",
        "시스템 레벨", "시스템 수준", "시스템급",
        "에너지 성능", "전력 소비", "소비전력",
        "계산 효율", "처리 효율", "연산 효율",
        "벤치마크", "성능 지표", "성능 측정",
        "열설계전력", "TDP"
    ],

    "TC-SC-440a.1": [
        # Materials Sourcing - Critical materials (영어)
        "critical material", "strategic material", "key material",
        "rare earth", "cobalt", "lithium", "tantalum", "gallium",
        "silicon", "germanium", "indium", "tungsten",
        "conflict mineral", "3TG", "tin", "gold",
        "supply risk", "material risk", "sourcing risk",
        "supply chain", "supply security", "material availability",
        "supply chain transparency", "traceability",
        "responsible sourcing", "ethical sourcing",
        "material scarcity", "resource availability",
        "due diligence", "supplier audit", "risk management",
        # Materials Sourcing - Critical materials (한국어)
        "핵심 소재", "핵심 자원", "중요 소재", "전략 소재",
        "희토류", "희소금속", "코발트", "리튬", "탄탈룸",
        "갈륨", "실리콘", "게르마늄", "인듐", "텅스텐",
        "분쟁광물", "분쟁 광물", "주석", "금",
        "공급 리스크", "공급 위험", "소재 위험", "조달 위험",
        "공급망", "공급 안정성", "소재 가용성", "자원 확보",
        "공급망 투명성", "추적가능성", "추적성",
        "책임 있는 조달", "책임조달", "윤리적 조달",
        "소재 부족", "자원 가용성", "자원 부족",
        "실사", "공급사 감사", "리스크 관리", "위험 관리"
    ],

    "TC-SC-520a.1": [
        # Intellectual Property Protection & Competitive Behaviour (영어)
        "monetary loss", "legal proceeding", "litigation",
        "anti-competitive", "antitrust", "competition law",
        "monopoly", "cartel", "price fixing",
        "market manipulation", "unfair competition",
        "fine", "penalty", "settlement", "damages",
        "regulatory action", "enforcement action",
        "intellectual property", "patent", "IP",
        "infringement", "violation", "breach",
        # Intellectual Property Protection & Competitive Behaviour (한국어)
        "금전적 손실", "금전 손실", "벌금",
        "법적 절차", "소송", "법적 조치",
        "반경쟁", "독과점", "경쟁법", "공정거래",
        "담합", "카르텔", "가격 담합", "가격 조작",
        "시장 조작", "불공정 경쟁", "부당 경쟁",
        "과태료", "과징금", "합의금", "손해배상",
        "규제 조치", "행정 조치", "제재",
        "지적재산권", "지적재산", "특허", "IP",
        "침해", "위반", "위법"
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
    print("SASB Semiconductors 메트릭별 키워드 매핑")
    print("=" * 60)

    for metric_id, keywords in METRIC_KEYWORDS.items():
        print(f"\n{metric_id}: {len(keywords)}개 키워드")
        print(f"  첫 8개: {', '.join(keywords[:8])}")

    print("\n" + "=" * 60)
    print(f"전체 고유 키워드 수: {len(get_all_keywords())}")
    print("=" * 60)
