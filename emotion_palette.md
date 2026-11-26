# 🎨 Emotion Palette 프로젝트 개발 대화 기록

> **프로젝트 요약:** 수업 자료(5단원 가치를 창출하는 소프트웨어) 및 수행평가(반응형 웹사이트 제작 & Pitch-Deck)를 바탕으로, 매시간 기록한 감정과 색상이 좌표 위에서 수채화처럼 번져 나만의 그라데이션 아트를 완성하는 **Streamlit 기반 반응형 웹 애플리케이션(`Emotion Palette`)** 개발 과정입니다.

---

## 1. 주제 탐색 및 아이디어 브레인스토밍

### 🙋 사용자 요청
* 수업 자료(`5. 가치를 창출하는 소프트웨어`)와 수행평가 안내(`반응형 웹사이트 제작`, `Pitch-Deck 발표`)를 공유하며 어떤 서비스를 만들지 함께 아이디어를 구상함.

### 💻 제안된 소프트웨어 프로젝트 아이디어 요약
1. **1차 제안 (수업 자료 기반 3종):**
   * 고대비·음성 안내 배리어프리 웹 키오스크
   * 우리 학교·동네 편의·안전 시설 공유 맵
   * 청소년 맞춤형 디지털 습관 & 헬스케어 대시보드
2. **2차 제안 (분야별 3종):**
   * 통학·대중교통 최적 경로 및 혼잡도 계산기
   * 스마트 반려식물·작물 생육 상태 진단 대시보드
   * 교내 공용 물품·학습 공간 실시간 예약 중개 웹
3. **3차 제안 (비즈니스 모델·일상 3종):**
   * 교내 중고 교재·준비물 매칭 & 자동 가격 산출 웹
   * 시험 대비 뽀모도로 타이머 & 과목별 학습량 분석 웹
   * 나만의 구독 서비스 지출 관리 & 효율 진단 대시보드
4. **4차 제안 (교육·협업·데이터 3종):**
   * 급식 영양 밸런스 계산 & 잔반 줄이기 시뮬레이터
   * 팀 프로젝트 역할 분담 & D-Day 진행률 트래커
   * 추천 알고리즘 & 가짜뉴스 판별 인터랙티브 퀴즈 웹
5. **5차 제안 (시뮬레이션·펀딩 3종):**
   * 가상 방 꾸미기 예산 & 가구 배치 시뮬레이터
   * 목표 달성 용돈 저축 & 소비 패턴 분석 트래커
   * 가상 포인트 기반 미니 크라우드 펀딩 웹 플랫폼
6. **6차 제안 (유틸리티·접근성 10종):**
   * AI 활용·저작권 윤리 자가 진단 체크리스트 웹
   * 1인 크리에이터 광고 수익 & 조회수 시뮬레이터
   * 날씨·미세먼지 조건별 맞춤형 운동 루틴 추천 웹
   * 음식점·카페 모바일 대기 번호표 & 예상 대기 시간 계산 웹
   * 우리 반 분실물 센터 & 습득물 키워드 매칭 웹
   * 분리배출 가이드 검색 & 환경 기여도 계산기
   * 맞춤형 웹 명함 & 개발자 포트폴리오 자동 생성기
   * 동아리·모임 회비 정산 및 1/N 더치페이 계산기
   * 저시력자·어르신을 위한 큰 글씨 복약 알림 & 시간표 웹
   * 코딩 키워드 타자 속도(CPM) & 정확도 측정 웹
7. **7차 제안 (보안·헬스·라이프스타일 10종 중 최종 선정):**
   * **10번 선택: 나만의 하루 감정 기록 & 컬러 팔레트 다이어리 웹**

---

## 2. 핵심 아이디어 구체화 및 사용자 설계

### 🙋 사용자 아이디어 및 스케치 정의
1. **시간별 감정 및 색상 기록:** 한 시간마다(하루 24번) 자신의 감정을 기록하고, 그에 어울리는 색상을 선택할 수 있음.
2. **5×5 시간표 그리드 & 자동 그라데이션:**
   * 가운데 칸을 제외한 24칸(`1`~`24`)의 `5×5` 격자 형태로 시간을 배치함.
   * 특정 칸에 색상을 기록하면, 기록된 좌표의 색상이 주변 빈칸까지 자연스럽게 확산되며 **자동으로 그라데이션을 생성**함.
3. **기간 확장 및 도형 마스킹:**
   * 조회 및 팔레트 범위를 **하루(24시간) → 일주일(1 week) → 한 달(1 month) → 일 년(1 year)**으로 확장 가능하게 구현.
   * 팔레트의 외곽 모형을 **하트(Heart), 별(Star), 원형(Circle), 네잎클로버(Clover), 둥근 사각형(Rounded Square)** 등으로 선택 가능하게 구성.

---

## 3. 1차 프로토타입 구현 (`main.py` v1)

### 🙋 기술 스택 및 알고리즘 요구사항
* **배포 환경:** Streamlit Cloud (`main.py`) 및 버전 숫자 없는 `requirements.txt` 제공.
* **그라데이션 알고리즘:** 좌표 기반 역거리 가중 보간(IDW) 그라데이션을 사용하되, 기록하지 않은 빈칸이 흰색으로 비어 보이지 않도록 색상이 넓게 퍼지게 구현.
* **입력 UI:** 대표 감정 선택과 세부 컬러 피커(`st.color_picker`) 동시 제공.

### 📦 `requirements.txt`
```text
streamlit
numpy
pillow
```

### ⚙️ 1차 구현 핵심 로직 요약
* `HOUR_TO_5X5_COORD`: 1시~24시를 `5×5` 격자 내 `(0.0 ~ 1.0)` 정규화 좌표로 매핑.
* `generate_emotion_palette()`: 하루 조회 시에는 `5×5` 좌표를 사용하고, 7일·30일·365일 조회 시에는 $X$축을 날짜 흐름, $Y$축을 시간대(1~24시)로 매핑하여 NumPy 벡터 연산으로 IDW 그라데이션 이미지를 합성.
* `create_shape_mask()`: 2배 슈퍼샘플링(Antialiasing)을 적용한 알파 채널 마스크로 도형 외곽선을 매끄럽게 자름.

---

## 4. UI/UX 전면 개편 및 인스타 감성 고도화 (`main-v2.py`)

### 🙋 15가지 세부 수정 요구사항
1. `"조회 및 팔레트 범위"` 문구를 **`"조회 기간"`**으로 변경.
2. `"조회 기간"` 선택 방식을 드롭다운 목록에서 **`24 hours` / `1 week` / `1 month` / `1 year`** 각각의 **파스텔 색깔 둥근 박스 버튼**으로 변경.
3. `"팔레트 모형"`은 목록 선택을 유지하되 한국어를 제거하고 **영어 도형 이름(`Rounded Square`, `Heart`, `Star`, `Circle`, `Clover`)**만 표시.
4. `"그라데이션 번짐 조절"` 항목을 삭제하고, 항상 **색상 경계 선명도 최저(`power=1.2`) + 수채화 블렌딩(`radius=18`)**이 유지되도록 고정.
5. `"빠른 테스트 & 시연 도구"`를 삭제하고 **`"전체 기록 초기화"`** 버튼만 남기며, 클릭 시 **`"정말 초기화 하시겠습니다? 한번 초기화하면 되돌릴 수 없습니다."`** 팝업창(`@st.dialog`) 출력.
6. 부제를 **`"Mapped hour by hour, your moments melt into a masterpiece."`**로 교체.
7. `"시간 별 감정 및 색상 기록"` 제목을 삭제하고, `1시~24시` 시간표 버튼에 **파스텔 배경과 은은한 네온 테두리(`box-shadow`)** 적용.
8. 입력 안내 문구를 **`"당신의 xx시는 어떤가요?"`**로 변경.
9. `"대표 감정 선택"`을 **`"대표 감정"`**으로 변경하고, 목록을 **`행복 / 설렘 / 평온 / 슬픔 / 화남 / 집중 / 열정 / 사랑 / 직접 선택`** 9종으로 재구성.
10. `"세부 색상 선택 (컬러 피커)"`를 **`"순간의 색깔"`**로 변경.
11. `"한 줄 메모 (선택 사항)"` 항목 삭제.
12. 결과 제목을 숫자 `2` 없이 **`"My Emotion Palette"`**로 변경.
13. 이미지 하단의 모형·기록 시간 캡션 삭제.
14. 하단 통계 카드(`기간 내 기록 수`, `가장 많이 느낀 감정`) 삭제.
15. 전체 타이포그래피를 고급스러운 **인스타 감성 에디토리얼 폰트(`Cormorant Garamond`, `Noto Serif KR`, `Pretendard`)**로 적용.

---

## 5. 최종 완성 코드 (`main.py`)

```python
import io
import json
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import streamlit as st

# ---------------------------------------------------------
# 1. 페이지 기본 설정 및 인스타 감성 반응형 CSS 스타일
# ---------------------------------------------------------
st.set_page_config(
    page_title="My Emotion Palette",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# 2. 상수 및 기본 데이터 정의 (대표 감정 9종 & 5x5 그리드)
# ---------------------------------------------------------
PRESET_EMOTIONS = {
    "행복": "#FFE066",
    "설렘": "#FF9EBB",
    "평온": "#8CE99A",
    "슬픔": "#74C0FC",
    "화남": "#FF6B6B",
    "집중": "#63E6BE",
    "열정": "#FFA94D",
    "사랑": "#F783AC",
    "직접 선택": "#B197FC",
}

# 스케치와 동일한 5x5 그리드 배치 (가운데 칸은 None)
GRID_5X5_LAYOUT = [
    [1, 2, 3, 4, 5],
    [6, 7, 8, 9, 10],
    [11, 12, None, 13, 14],
    [15, 16, 17, 18, 19],
    [20, 21, 22, 23, 24],
]

# 시간(1~24) -> (x, y) 정규화 좌표 매핑 (0.0 ~ 1.0)
HOUR_TO_5X5_COORD = {}
for r_idx, row in enumerate(GRID_5X5_LAYOUT):
    for c_idx, hr in enumerate(row):
        if hr is not None:
            HOUR_TO_5X5_COORD[hr] = (c_idx / 4.0, r_idx / 4.0)

PERIOD_OPTIONS = [
    {"label": "24 hours", "days": 1},
    {"label": "1 week", "days": 7},
    {"label": "1 month", "days": 30},
    {"label": "1 year", "days": 365},
]

SHAPE_OPTIONS = [
    "Rounded Square",
    "Heart",
    "Star",
    "Circle",
    "Clover",
]


# ---------------------------------------------------------
# 3. 유틸리티 함수 (색상 변환, 그라데이션 & 도형 생성)
# ---------------------------------------------------------
def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def get_contrast_text_color(hex_color: str) -> str:
    r, g, b = hex_to_rgb(hex_color)
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return "#2B2629" if luminance > 0.62 else "#FFFFFF"


def init_session_state():
    if "records" not in st.session_state:
        st.session_state.records = {}
    if "selected_hour" not in st.session_state:
        st.session_state.selected_hour = 1
    if "selected_day" not in st.session_state:
        st.session_state.selected_day = 0
    if "selected_period" not in st.session_state:
        st.session_state.selected_period = "24 hours"
    if "confirm_reset_fallback" not in st.session_state:
        st.session_state.confirm_reset_fallback = False


def inject_custom_css(selected_period: str):
    """고급스러운 인스타 감성 폰트, 파스텔 기간 버튼, 은은한 네온 시간표 CSS를 적용합니다."""
    active_map = {
        "24 hours": (1, 1, "#E57A9B"),
        "1 week": (1, 2, "#E0A44C"),
        "1 month": (2, 1, "#55B383"),
        "1 year": (2, 2, "#7A8CE8"),
    }
    act_row, act_col, act_ring = active_map.get(selected_period, (1, 1, "#E57A9B"))
    row_plus = "+ div" if act_row == 1 else "+ div + div"

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600&family=Noto+Serif+KR:wght@400;500;600;700&display=swap');
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

        html, body, [class*="css"] {{
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
            color: #2D272B;
        }}

        [data-testid="stAppViewContainer"] {{
            background: radial-gradient(circle at 12% 15%, #FFF5F8 0%, #FDFBF7 45%, #F4F7FF 100%);
        }}

        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #FFF9FB 0%, #F8F6FF 100%);
            border-right: 1px solid rgba(226, 208, 224, 0.55);
        }}

        .block-container {{
            padding-top: 2rem;
            padding-bottom: 2.5rem;
            max-width: 1180px;
        }}

        .hero-title {{
            font-family: 'Cormorant Garamond', 'Noto Serif KR', serif;
            font-size: clamp(2.1rem, 4vw, 3.0rem);
            font-weight: 700;
            letter-spacing: -0.01em;
            color: #241E22;
            line-height: 1.15;
            margin-bottom: 0.35rem;
        }}

        .hero-subtitle {{
            font-family: 'Cormorant Garamond', Georgia, serif;
            font-style: italic;
            font-size: clamp(1.08rem, 1.8vw, 1.32rem);
            color: #7A6B74;
            letter-spacing: 0.01em;
            margin-bottom: 1.6rem;
        }}

        .section-heading-editorial {{
            font-family: 'Cormorant Garamond', 'Noto Serif KR', serif;
            font-size: clamp(1.45rem, 2.3vw, 1.85rem);
            font-weight: 600;
            color: #2A2226;
            letter-spacing: 0.01em;
            margin-bottom: 0.75rem;
        }}

        .sidebar-section-label {{
            font-family: 'Noto Serif KR', 'Pretendard', serif;
            font-size: 0.96rem;
            font-weight: 600;
            color: #3D3238;
            margin-bottom: 0.45rem;
            letter-spacing: 0.02em;
        }}

        .question-prompt {{
            font-family: 'Noto Serif KR', 'Pretendard', serif;
            font-size: 1.15rem;
            font-weight: 600;
            color: #2F252A;
            margin-top: 0.4rem;
            margin-bottom: 0.65rem;
        }}

        /* 사이드바: 조회 기간 파스텔 둥근 박스 버튼 4종 */
        [data-testid="stSidebar"] div:has(.period-section-anchor) + div button,
        [data-testid="stSidebar"] div:has(.period-section-anchor) + div + div button {{
            font-family: 'Cormorant Garamond', serif !important;
            font-size: 1.05rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.02em !important;
            border-radius: 16px !important;
            padding: 0.55rem 0.4rem !important;
            transition: all 0.22s ease !important;
        }}

        [data-testid="stSidebar"] div:has(.period-section-anchor) + div [data-testid="stColumn"]:nth-child(1) button,
        [data-testid="stSidebar"] div:has(.period-section-anchor) + div [data-testid="column"]:nth-child(1) button {{
            background: linear-gradient(135deg, #FFE5EC 0%, #FFD6E2 100%) !important;
            color: #6B2D41 !important;
            border: 1.5px solid #F7B5C8 !important;
        }}

        [data-testid="stSidebar"] div:has(.period-section-anchor) + div [data-testid="stColumn"]:nth-child(2) button,
        [data-testid="stSidebar"] div:has(.period-section-anchor) + div [data-testid="column"]:nth-child(2) button {{
            background: linear-gradient(135deg, #FFF3D6 0%, #FFE7BA 100%) !important;
            color: #6B4C1E !important;
            border: 1.5px solid #F5CF8E !important;
        }}

        [data-testid="stSidebar"] div:has(.period-section-anchor) + div + div [data-testid="stColumn"]:nth-child(1) button,
        [data-testid="stSidebar"] div:has(.period-section-anchor) + div + div [data-testid="column"]:nth-child(1) button {{
            background: linear-gradient(135deg, #E2F7EC 0%, #CBEFDE 100%) !important;
            color: #245740 !important;
            border: 1.5px solid #9AD9BC !important;
        }}

        [data-testid="stSidebar"] div:has(.period-section-anchor) + div + div [data-testid="stColumn"]:nth-child(2) button,
        [data-testid="stSidebar"] div:has(.period-section-anchor) + div + div [data-testid="column"]:nth-child(2) button {{
            background: linear-gradient(135deg, #E6EAFF 0%, #D6DEFF 100%) !important;
            color: #323D73 !important;
            border: 1.5px solid #ACB8F7 !important;
        }}

        [data-testid="stSidebar"] div:has(.period-section-anchor) {row_plus} [data-testid="stColumn"]:nth-child({act_col}) button,
        [data-testid="stSidebar"] div:has(.period-section-anchor) {row_plus} [data-testid="column"]:nth-child({act_col}) button {{
            box-shadow: 0 0 0 2.5px {act_ring}, 0 6px 14px rgba(120, 100, 130, 0.18) !important;
            transform: translateY(-1px);
        }}

        /* 5x5 시간표 버튼: 파스텔 배경 + 은은한 네온 테두리 */
        div:has(.grid-section-anchor) + div button,
        div:has(.grid-section-anchor) + div + div button,
        div:has(.grid-section-anchor) + div + div + div button,
        div:has(.grid-section-anchor) + div + div + div + div button,
        div:has(.grid-section-anchor) + div + div + div + div + div button {{
            background: linear-gradient(145deg, #FFF7FB 0%, #F4F7FF 100%) !important;
            color: #3B3038 !important;
            font-family: 'Pretendard', sans-serif !important;
            font-weight: 600 !important;
            font-size: 0.88rem !important;
            border-radius: 14px !important;
            border: 1.5px solid rgba(203, 166, 255, 0.85) !important;
            box-shadow:
                0 0 8px rgba(255, 163, 207, 0.42),
                0 0 14px rgba(150, 204, 255, 0.38),
                inset 0 0 8px rgba(255, 255, 255, 0.9) !important;
            transition: all 0.2s ease !important;
        }}

        div:has(.grid-section-anchor) + div button:hover,
        div:has(.grid-section-anchor) + div + div button:hover,
        div:has(.grid-section-anchor) + div + div + div button:hover,
        div:has(.grid-section-anchor) + div + div + div + div button:hover,
        div:has(.grid-section-anchor) + div + div + div + div + div button:hover {{
            background: linear-gradient(145deg, #FFEBF4 0%, #E8F0FF 100%) !important;
            border-color: #FF8EC7 !important;
            box-shadow:
                0 0 12px rgba(255, 130, 195, 0.72),
                0 0 22px rgba(130, 188, 255, 0.62) !important;
            transform: translateY(-1.5px);
        }}

        .center-badge {{
            display: flex;
            align-items: center;
            justify-content: center;
            height: 42px;
            border-radius: 14px;
            background: linear-gradient(135deg, #FFD6E7 0%, #FBE8FF 50%, #D8E8FF 100%);
            border: 1.5px solid rgba(214, 178, 255, 0.85);
            box-shadow: 0 0 10px rgba(255, 175, 215, 0.45);
            color: #4A3846;
            font-family: 'Cormorant Garamond', serif;
            font-weight: 700;
            font-size: 0.95rem;
            letter-spacing: 0.04em;
        }}

        .slot-preview {{
            border-radius: 10px;
            padding: 3px 6px;
            text-align: center;
            font-size: 0.74rem;
            font-weight: 600;
            margin-top: -6px;
            margin-bottom: 8px;
            letter-spacing: 0.01em;
            transition: all 0.2s ease;
        }}

        .slot-empty {{
            background: rgba(255, 245, 250, 0.65);
            color: #B4A5AE;
            border: 1px dashed rgba(210, 185, 215, 0.65);
        }}

        @media (max-width: 768px) {{
            .block-container {{
                padding-left: 0.9rem;
                padding-right: 0.9rem;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def create_shape_mask(size: int, shape_name: str) -> Image.Image:
    """안티에일리어싱이 적용된 고해상도 도형 알파 마스크(L 모드)를 생성합니다."""
    ss_size = size * 2
    mask = Image.new("L", (ss_size, ss_size), 0)

    if shape_name == "Rounded Square":
        draw = ImageDraw.Draw(mask)
        pad = int(ss_size * 0.04)
        radius = int(ss_size * 0.15)
        draw.rounded_rectangle(
            [pad, pad, ss_size - pad, ss_size - pad], radius=radius, fill=255
        )

    elif shape_name == "Circle":
        draw = ImageDraw.Draw(mask)
        pad = int(ss_size * 0.04)
        draw.ellipse([pad, pad, ss_size - pad, ss_size - pad], fill=255)

    elif shape_name == "Star":
        draw = ImageDraw.Draw(mask)
        cx, cy = ss_size / 2, ss_size / 2
        outer_r = ss_size * 0.46
        inner_r = outer_r * 0.43
        points = []
        for i in range(10):
            angle = -math.pi / 2 + i * (math.pi / 5)
            r = outer_r if i % 2 == 0 else inner_r
            points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
        draw.polygon(points, fill=255)

    elif shape_name == "Heart":
        y_idx, x_idx = np.ogrid[:ss_size, :ss_size]
        x = (x_idx - ss_size / 2) / (ss_size * 0.38)
        y = (ss_size * 0.46 - y_idx) / (ss_size * 0.38)
        heart_eq = (x**2 + y**2 - 1) ** 3 - (x**2) * (y**3)
        arr = np.where(heart_eq <= 0, 255, 0).astype(np.uint8)
        mask = Image.fromarray(arr, mode="L")

    elif shape_name == "Clover":
        y_idx, x_idx = np.ogrid[:ss_size, :ss_size]
        x = (x_idx - ss_size / 2) / (ss_size * 0.46)
        y = (y_idx - ss_size / 2) / (ss_size * 0.46)
        r = np.sqrt(x**2 + y**2)
        theta = np.arctan2(y, x)
        clover_boundary = 0.25 + 0.72 * np.abs(np.sin(2 * theta))
        arr = np.where(r <= clover_boundary, 255, 0).astype(np.uint8)
        mask = Image.fromarray(arr, mode="L")

    return mask.resize((size, size), resample=Image.Resampling.LANCZOS)


def generate_emotion_palette(
    records: dict,
    days_range: int,
    shape_name: str,
    canvas_size: int = 500,
) -> Image.Image:
    """
    기록된 (날짜, 시간, 색상) 좌표를 기반으로 역거리 가중 보간(IDW) 그라데이션을 생성합니다.
    """
    points = []

    for key, val in records.items():
        day_str, hour_str = key.split("_")
        day_idx = int(day_str)
        hour_idx = int(hour_str)

        if 0 <= day_idx < days_range and 1 <= hour_idx <= 24:
            rgb = hex_to_rgb(val["color"])
            if days_range == 1:
                nx, ny = HOUR_TO_5X5_COORD[hour_idx]
            else:
                nx = day_idx / max(1, days_range - 1)
                ny = (hour_idx - 1) / 23.0
            points.append((nx, ny, rgb))

    if not points:
        y_grid, x_grid = np.mgrid[0:canvas_size, 0:canvas_size] / float(canvas_size)
        r = (250 - 12 * y_grid + 4 * x_grid).astype(np.uint8)
        g = (232 + 10 * x_grid - 6 * y_grid).astype(np.uint8)
        b = (242 + 12 * y_grid).astype(np.uint8)
        base_img = Image.fromarray(np.dstack([r, g, b]), mode="RGB")
    else:
        if len(points) > 120:
            bins = {}
            for nx, ny, rgb in points:
                bx = min(49, int(nx * 50))
                by = min(49, int(ny * 50))
                bins.setdefault((bx, by), []).append((nx, ny, rgb))
            aggregated = []
            for cell_pts in bins.values():
                avg_x = sum(p[0] for p in cell_pts) / len(cell_pts)
                avg_y = sum(p[1] for p in cell_pts) / len(cell_pts)
                avg_r = sum(p[2][0] for p in cell_pts) / len(cell_pts)
                avg_g = sum(p[2][1] for p in cell_pts) / len(cell_pts)
                avg_b = sum(p[2][2] for p in cell_pts) / len(cell_pts)
                aggregated.append((avg_x, avg_y, (avg_r, avg_g, avg_b)))
            points = aggregated

        coords = np.array([[0.08 + 0.84 * p[0], 0.08 + 0.84 * p[1]] for p in points])
        colors = np.array([p[2] for p in points], dtype=np.float32)

        lin = np.linspace(0.0, 1.0, canvas_size, dtype=np.float32)
        grid_x, grid_y = np.meshgrid(lin, lin)

        power = 1.2
        dx = grid_x[:, :, None] - coords[None, None, :, 0]
        dy = grid_y[:, :, None] - coords[None, None, :, 1]
        dist_sq = dx**2 + dy**2 + 0.014
        weights = 1.0 / np.power(dist_sq, power / 2.0)

        weight_sum = np.sum(weights, axis=2, keepdims=True)
        norm_weights = weights / weight_sum

        blended_rgb = np.einsum("ijk,kl->ijl", norm_weights, colors)
        blended_rgb = np.clip(blended_rgb, 0, 255).astype(np.uint8)

        base_img = Image.fromarray(blended_rgb, mode="RGB")
        base_img = base_img.filter(ImageFilter.GaussianBlur(radius=18))

    rgba_img = base_img.convert("RGBA")
    shape_mask = create_shape_mask(canvas_size, shape_name)
    rgba_img.putalpha(shape_mask)
    return rgba_img


# ---------------------------------------------------------
# 4. 초기화 확인 팝업 다이얼로그
# ---------------------------------------------------------
if hasattr(st, "dialog"):

    @st.dialog("초기화 확인")
    def show_reset_dialog():
        st.write("정말 초기화 하시겠습니다? 한번 초기화하면 되돌릴 수 없습니다.")
        col_yes, col_no = st.columns(2)
        with col_yes:
            if st.button("초기화", type="primary", use_container_width=True):
                st.session_state.records = {}
                st.session_state.selected_hour = 1
                st.session_state.selected_day = 0
                st.rerun()
        with col_no:
            if st.button("취소", use_container_width=True):
                st.rerun()


# ---------------------------------------------------------
# 5. 메인 UI 구성
# ---------------------------------------------------------
def main():
    init_session_state()
    inject_custom_css(st.session_state.selected_period)

    st.markdown('<div class="hero-title">Emotion Palette</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">Mapped hour by hour, your moments melt into a masterpiece.</div>',
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown('<div class="sidebar-section-label">조회 기간</div>', unsafe_allow_html=True)
        st.markdown('<div class="period-section-anchor"></div>', unsafe_allow_html=True)

        p_row1 = st.columns(2, gap="small")
        with p_row1[0]:
            if st.button("24 hours", key="period_btn_24h", use_container_width=True):
                st.session_state.selected_period = "24 hours"
                st.rerun()
        with p_row1[1]:
            if st.button("1 week", key="period_btn_1w", use_container_width=True):
                st.session_state.selected_period = "1 week"
                st.rerun()

        p_row2 = st.columns(2, gap="small")
        with p_row2[0]:
            if st.button("1 month", key="period_btn_1m", use_container_width=True):
                st.session_state.selected_period = "1 month"
                st.rerun()
        with p_row2[1]:
            if st.button("1 year", key="period_btn_1y", use_container_width=True):
                st.session_state.selected_period = "1 year"
                st.rerun()

        days_range = next(
            item["days"]
            for item in PERIOD_OPTIONS
            if item["label"] == st.session_state.selected_period
        )

        st.markdown("<div style='height: 0.6rem;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="sidebar-section-label">팔레트 모형</div>', unsafe_allow_html=True)
        selected_shape = st.selectbox(
            "팔레트 모형",
            SHAPE_OPTIONS,
            index=0,
            label_visibility="collapsed",
        )

        st.divider()

        if st.button("전체 기록 초기화", use_container_width=True):
            if hasattr(st, "dialog"):
                show_reset_dialog()
            else:
                st.session_state.confirm_reset_fallback = True

        if st.session_state.confirm_reset_fallback:
            st.warning("정말 초기화 하시겠습니다? 한번 초기화하면 되돌릴 수 없습니다.")
            fb_c1, fb_c2 = st.columns(2)
            with fb_c1:
                if st.button("초기화", type="primary", use_container_width=True):
                    st.session_state.records = {}
                    st.session_state.confirm_reset_fallback = False
                    st.rerun()
            with fb_c2:
                if st.button("취소", use_container_width=True):
                    st.session_state.confirm_reset_fallback = False
                    st.rerun()

        with st.expander("데이터 백업 / 불러오기"):
            json_str = json.dumps(st.session_state.records, ensure_ascii=False, indent=2)
            st.download_button(
                label="JSON 백업 다운로드",
                data=json_str,
                file_name="emotion_records.json",
                mime="application/json",
                use_container_width=True,
            )
            uploaded_file = st.file_uploader("JSON 불러오기", type=["json"])
            if uploaded_file is not None:
                try:
                    loaded = json.load(uploaded_file)
                    if isinstance(loaded, dict):
                        st.session_state.records = loaded
                        st.success("기록을 불러왔습니다.")
                except Exception:
                    st.error("올바른 JSON 파일이 아닙니다.")

    left_col, right_col = st.columns([1.15, 1.0], gap="large")

    with left_col:
        if days_range > 1:
            day_idx = (
                st.slider(
                    "기록할 날짜 선택 (Day 1 = 오늘)",
                    min_value=1,
                    max_value=days_range,
                    value=min(st.session_state.selected_day + 1, days_range),
                )
                - 1
            )
            st.session_state.selected_day = day_idx
        else:
            st.session_state.selected_day = 0

        current_day = st.session_state.selected_day

        st.markdown('<div class="grid-section-anchor"></div>', unsafe_allow_html=True)

        for row in GRID_5X5_LAYOUT:
            cols = st.columns(5, gap="small")
            for c_idx, hr in enumerate(row):
                with cols[c_idx]:
                    if hr is None:
                        st.markdown('<div class="center-badge">24H</div>', unsafe_allow_html=True)
                    else:
                        rec_key = f"{current_day}_{hr}"
                        rec = st.session_state.records.get(rec_key)
                        is_selected = st.session_state.selected_hour == hr
                        btn_label = f"✦ {hr}시" if is_selected else f"{hr}시"
                        if st.button(
                            btn_label,
                            key=f"grid_btn_{current_day}_{hr}",
                            use_container_width=True,
                        ):
                            st.session_state.selected_hour = hr
                            st.rerun()

                        if rec:
                            bg = rec["color"]
                            fg = get_contrast_text_color(bg)
                            emo_text = rec["emotion"]
                            st.markdown(
                                f'<div class="slot-preview" style="background:{bg}; color:{fg}; box-shadow: 0 2px 8px {bg}66;">{emo_text}</div>',
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown(
                                '<div class="slot-preview slot-empty">·</div>',
                                unsafe_allow_html=True,
                            )

        st.divider()

        target_hr = st.session_state.selected_hour
        target_key = f"{current_day}_{target_hr}"
        existing = st.session_state.records.get(target_key)

        prompt_text = (
            f"당신의 {target_hr}시는 어떤가요?"
            if days_range == 1
            else f"Day {current_day + 1} · 당신의 {target_hr}시는 어떤가요?"
        )
        st.markdown(f'<div class="question-prompt">{prompt_text}</div>', unsafe_allow_html=True)

        in_col1, in_col2 = st.columns([1.4, 1.0])
        with in_col1:
            default_emo_idx = 0
            if existing and existing["emotion"] in PRESET_EMOTIONS:
                default_emo_idx = list(PRESET_EMOTIONS.keys()).index(existing["emotion"])
            chosen_emotion = st.selectbox(
                "대표 감정",
                list(PRESET_EMOTIONS.keys()),
                index=default_emo_idx,
            )

        with in_col2:
            preset_hex = PRESET_EMOTIONS[chosen_emotion]
            if existing and existing["emotion"] == chosen_emotion:
                initial_hex = existing["color"]
            else:
                initial_hex = preset_hex

            chosen_color = st.color_picker(
                "순간의 색깔",
                value=initial_hex,
                key=f"cp_{target_key}_{chosen_emotion}",
            )

        act_col1, act_col2 = st.columns(2)
        with act_col1:
            if st.button("기록 저장하기", type="primary", use_container_width=True):
                st.session_state.records[target_key] = {
                    "emotion": chosen_emotion,
                    "color": chosen_color,
                }
                if target_hr < 24:
                    st.session_state.selected_hour = target_hr + 1
                st.rerun()

        with act_col2:
            if st.button("선택 시간 지우기", use_container_width=True):
                if target_key in st.session_state.records:
                    del st.session_state.records[target_key]
                    st.rerun()

    with right_col:
        st.markdown(
            '<div class="section-heading-editorial">My Emotion Palette</div>',
            unsafe_allow_html=True,
        )

        palette_img = generate_emotion_palette(
            records=st.session_state.records,
            days_range=days_range,
            shape_name=selected_shape,
            canvas_size=500,
        )

        st.image(palette_img, use_container_width=True)

        img_buffer = io.BytesIO()
        palette_img.save(img_buffer, format="PNG")
        st.download_button(
            label="Save Palette (PNG)",
            data=img_buffer.getvalue(),
            file_name=f"my_emotion_palette_{days_range}d.png",
            mime="image/png",
            use_container_width=True,
        )


if __name__ == "__main__":
    main()
```

---

## 6. 배포 및 실행 가이드

1. GitHub 저장소 루트 디렉터리에 **`main.py`**와 **`requirements.txt`** 두 파일을 업로드합니다.
2. [Streamlit Community Cloud](https://share.streamlit.io/)에서 해당 저장소와 `main.py` 경로를 지정해 배포합니다.
3. 수행평가 보고서나 AI 활용 기록을 작성할 때 이 문서를 참고하여 **문제 정의 → 알고리즘 설계(IDW 좌표 보간 및 도형 마스킹) → UI/UX 고도화 과정**을 논리적으로 정리할 수 있습니다.