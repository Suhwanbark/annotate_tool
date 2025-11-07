#!/usr/bin/env python3
"""메트릭별 키워드 매핑 - SASB Automobiles (TR-AU)"""

METRIC_KEYWORDS = {
    "TR-AU-250a.1": [
        # Product Safety - NCAP 5-star rating
        "NCAP", "안전등급", "안전성", "5성", "별점", "충돌테스트", "충돌시험",
        "안전평가", "안전도", "safety rating", "5-star", "crash test",
        "Euro NCAP", "KNCAP", "한국", "유럽", "미국", "IIHS",
        "차량안전", "안전성능", "평가등급", "최고등급", "탑세이프티",
    ],

    "TR-AU-250a.2": [
        # Product Safety - defect complaints
        "결함", "리콜", "신고", "불만", "민원", "조사", "하자", "품질",
        "안전결함", "제품결함", "결함신고", "고객불만", "품질문제",
        "조사비율", "complaint", "defect", "investigation",
        "안전성문제", "제품안전", "소비자보호", "시정조치",
    ],

    "TR-AU-250a.3": [
        # Product Safety - recalls
        "리콜", "회수", "결함", "시정조치", "자발적리콜", "강제리콜",
        "차량리콜", "recall", "리콜대수", "리콜건수", "안전리콜",
        "품질리콜", "제품회수", "무상수리", "교환", "환불",
        "시정명령", "국토부", "NHTSA",
    ],

    "TR-AU-310a.1": [
        # Labour Practices - collective agreements
        "단체협약", "노조", "노동조합", "임금협상", "단협", "근로자",
        "노사협의", "collective agreement", "union", "workforce",
        "노조가입률", "조합원", "단체교섭", "임금", "근로조건",
        "노사관계", "노사협력", "고용", "정규직", "비정규직",
    ],

    "TR-AU-310a.2": [
        # Labour Practices - work stoppages
        "파업", "쟁의", "노사분규", "작업중단", "휴무", "노동쟁의",
        "strike", "work stoppage", "파업일수", "조업중단",
        "쟁의행위", "근로손실", "생산중단", "노사갈등",
        "노동운동", "집단행동", "대규모파업",
    ],

    "TR-AU-410a.1": [
        # Fuel Economy & Use-phase Emissions - fleet fuel economy
        "연비", "배출량", "CO2", "온실가스", "탄소배출", "이산화탄소",
        "fuel economy", "mpg", "L/km", "km/L", "g/km", "gCO2",
        "평균연비", "판매가중", "연료효율", "연료소비",
        "배기가스", "탄소중립", "저탄소", "배출기준", "CAFE",
        "기업평균연비", "Fleet", "지역별", "region",
    ],

    "TR-AU-410a.2": [
        # Fuel Economy & Use-phase Emissions - ZEV/hybrid sales
        "전기차", "하이브리드", "무공해차", "ZEV", "EV", "친환경차",
        "zero emission", "electric vehicle", "플러그인", "plug-in",
        "PHEV", "HEV", "BEV", "수소차", "FCEV", "연료전지",
        "전동화", "전기자동차", "하이브리드차", "판매대수",
        "친환경차량", "무배출차", "배터리차", "e-모빌리티",
    ],

    "TR-AU-410a.3": [
        # Fuel Economy & Use-phase Emissions - strategy
        "연비전략", "배출량전략", "탄소감축", "목표", "로드맵",
        "전동화전략", "친환경전략", "저탄소전략", "배출관리",
        "strategy", "emissions", "fuel economy", "risk", "opportunity",
        "계획", "중장기전략", "탄소중립목표", "2050", "넷제로",
        "전환전략", "저배출", "대응방안", "기회", "위험관리",
    ],

    "TR-AU-440a.1": [
        # Materials Sourcing - critical materials
        "원자재", "희토류", "광물", "리튬", "코발트", "니켈",
        "critical materials", "raw materials", "rare earth",
        "공급망", "조달", "자재관리", "희소금속", "전략광물",
        "배터리원료", "핵심광물", "공급위험", "자원안보",
        "윤리적조달", "분쟁광물", "supply chain", "sourcing",
        "채굴", "추적가능성", "투명성", "인권", "환경영향",
    ],

    "TR-AU-440b.1": [
        # Materials Efficiency & Recycling - manufacturing waste
        "폐기물", "재활용", "제조폐기물", "생산폐기물", "waste",
        "manufacturing waste", "recycled", "재활용률", "처리",
        "발생량", "metric tonnes", "톤", "t", "%", "퍼센트",
        "폐기물관리", "자원순환", "순환경제", "감량", "재사용",
        "생산공정", "공장", "제조시설", "폐기물처리",
    ],

    "TR-AU-440b.2": [
        # Materials Efficiency & Recycling - end-of-life material
        "폐차", "수명종료", "재활용", "회수", "end-of-life", "EOL",
        "폐차재활용", "차량회수", "재활용률", "회수율",
        "recovered", "material recovery", "폐차처리",
        "metric tonnes", "톤", "t", "%", "퍼센트",
        "순환경제", "자원회수", "재자원화", "폐차장",
    ],

    "TR-AU-440b.3": [
        # Materials Efficiency & Recycling - average recyclability
        "재활용성", "재활용률", "회수율", "recyclability", "average",
        "평균재활용성", "판매가중", "sales-weighted",
        "재활용가능성", "분해성", "재사용", "순환성",
        "설계단계", "친환경설계", "재활용설계", "DfR",
        "자원순환", "%", "퍼센트", "톤", "metric tonnes",
    ],
}
