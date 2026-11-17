import io
import json
import math
import random
from datetime import datetime
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import streamlit as st

# ---------------------------------------------------------
# 1. 페이지 기본 설정 및 반응형 CSS 스타일
# ---------------------------------------------------------
st.set_page_config(
    page_title="감정 팔레트 | Emotion Palette",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    /* 반응형 레이아웃 및 카드 디자인 */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    .main-title {
        font-size: clamp(1.6rem, 3vw, 2.3rem);
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: clamp(0.95rem, 1.5vw, 1.1rem);
        color: #666666;
        margin-bottom: 1.2rem;
    }
    .center-badge {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 44px;
        border-radius: 10px;
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #a1c4fd 100%);
        color: #222222;
        font-weight: 700;
        font-size: 0.85rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    }
    .slot-preview {
        border-radius: 8px;
        padding: 4px 6px;
        text-align: center;
        font-size: 0.78rem;
        font-weight: 600;
        margin-top: -8px;
        margin-bottom: 8px;
        border: 1px solid rgba(0,0,0,0.08);
    }
    .stat-card {
        background-color: rgba(128, 128, 128, 0.08);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        margin-bottom: 0.8rem;
    }
    @media (max-width: 768px) {
        .block-container {
            padding-left: 0.8rem;
            padding-right: 0.8rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 2. 상수 및 기본 데이터 정의 (대표 감정 & 5x5 그리드 배치)
# ---------------------------------------------------------
PRESET_EMOTIONS = {
    "😊 기쁨 / 행복": "#FFD43B",
    "🥰 설렘 / 사랑": "#FF6B8B",
    "🌿 평온 / 힐링": "#51CF66",
    "😢 슬픔 / 우울": "#339AF0",
    "😡 화남 / 스트레스": "#FF4D4D",
    "😴 피곤 / 무기력": "#9775FA",
    "🤔 집중 / 차분": "#20C997",
    "🎨 직접 색상 선택": "#FF922B",
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

RANGE_OPTIONS = {
    "하루 (24시간)": 1,
    "일주일 (7일)": 7,
    "한 달 (30일)": 30,
    "일 년 (365일)": 365,
}

SHAPE_OPTIONS = [
    "둥근 사각형 (기본)",
    "하트 (Heart)",
    "별 (Star)",
    "원형 (Circle)",
    "네잎클로버 (Clover)",
]


# ---------------------------------------------------------
# 3. 유틸리티 함수 (색상 변환, 샘플 데이터, 그라데이션 & 도형 생성)
# ---------------------------------------------------------
def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def get_contrast_text_color(hex_color: str) -> str:
    r, g, b = hex_to_rgb(hex_color)
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return "#111111" if luminance > 0.6 else "#FFFFFF"


def init_session_state():
    if "records" not in st.session_state:
        st.session_state.records = {}
    if "selected_hour" not in st.session_state:
        st.session_state.selected_hour = 1
    if "selected_day" not in st.session_state:
        st.session_state.selected_day = 0


def load_sketch_example():
    """스케치 예시(3시 빨강, 11시 파랑, 12시 주황, 22시 초록)를 재현합니다."""
    st.session_state.records = {
        "0_3": {"emotion": "😡 화남 / 스트레스", "color": "#E03131", "note": "스케치 예시 1"},
        "0_11": {"emotion": "😢 슬픔 / 우울", "color": "#228BE6", "note": "스케치 예시 2"},
        "0_12": {"emotion": "🎨 직접 색상 선택", "color": "#F76707", "note": "스케치 예시 3"},
        "0_22": {"emotion": "🌿 평온 / 힐링", "color": "#66A80F", "note": "스케치 예시 4"},
    }
    st.session_state.selected_day = 0


def load_period_sample_data(days: int):
    """선택한 기간(1일/7일/30일/365일)에 맞춰 자연스러운 감정 샘플 데이터를 생성합니다."""
    emotion_pool = [
        ("😊 기쁨 / 행복", "#FFD43B"),
        ("🥰 설렘 / 사랑", "#FF6B8B"),
        ("🌿 평온 / 힐링", "#51CF66"),
        ("😢 슬픔 / 우울", "#339AF0"),
        ("😡 화남 / 스트레스", "#FF4D4D"),
        ("😴 피곤 / 무기력", "#9775FA"),
        ("🤔 집중 / 차분", "#20C997"),
    ]
    new_records = {}
    rng = random.Random(42)

    for d in range(days):
        sample_count = rng.randint(10, 17) if days <= 7 else rng.randint(6, 12)
        hours = rng.sample(range(1, 25), sample_count)
        dominant_idx = (d // max(1, days // 7)) % len(emotion_pool)
        for h in hours:
            if rng.random() < 0.55:
                emo, col = emotion_pool[dominant_idx]
            else:
                emo, col = rng.choice(emotion_pool)
            new_records[f"{d}_{h}"] = {
                "emotion": emo,
                "color": col,
                "note": f"Day {d + 1} - {h}시 기록",
            }
    st.session_state.records = new_records
    st.session_state.selected_day = 0


def create_shape_mask(size: int, shape_name: str) -> Image.Image:
    """안티에일리어싱이 적용된 고해상도 도형 알파 마스크(L 모드)를 생성합니다."""
    ss_size = size * 2
    mask = Image.new("L", (ss_size, ss_size), 0)

    if shape_name == "둥근 사각형 (기본)":
        draw = ImageDraw.Draw(mask)
        pad = int(ss_size * 0.04)
        radius = int(ss_size * 0.14)
        draw.rounded_rectangle(
            [pad, pad, ss_size - pad, ss_size - pad], radius=radius, fill=255
        )

    elif shape_name == "원형 (Circle)":
        draw = ImageDraw.Draw(mask)
        pad = int(ss_size * 0.04)
        draw.ellipse([pad, pad, ss_size - pad, ss_size - pad], fill=255)

    elif shape_name == "별 (Star)":
        draw = ImageDraw.Draw(mask)
        cx, cy = ss_size / 2, ss_size / 2
        outer_r = ss_size * 0.46
        inner_r = outer_r * 0.42
        points = []
        for i in range(10):
            angle = -math.pi / 2 + i * (math.pi / 5)
            r = outer_r if i % 2 == 0 else inner_r
            points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
        draw.polygon(points, fill=255)

    elif shape_name == "하트 (Heart)":
        y_idx, x_idx = np.ogrid[:ss_size, :ss_size]
        x = (x_idx - ss_size / 2) / (ss_size * 0.38)
        y = (ss_size * 0.46 - y_idx) / (ss_size * 0.38)
        heart_eq = (x**2 + y**2 - 1) ** 3 - (x**2) * (y**3)
        arr = np.where(heart_eq <= 0, 255, 0).astype(np.uint8)
        mask = Image.fromarray(arr, mode="L")

    elif shape_name == "네잎클로버 (Clover)":
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
    power: float = 2.1,
    blur_radius: int = 8,
    canvas_size: int = 480,
) -> tuple[Image.Image, list[dict]]:
    """
    기록된 (날짜, 시간, 색상) 좌표를 기반으로 역거리 가중 보간(IDW) 그라데이션을 생성합니다.
    기록되지 않은 칸도 주변 기록 색상이 자연스럽게 확산되어 흰색 공백을 최소화합니다.
    """
    points = []
    matched_records = []

    for key, val in records.items():
        day_str, hour_str = key.split("_")
        day_idx = int(day_str)
        hour_idx = int(hour_str)

        if 0 <= day_idx < days_range and 1 <= hour_idx <= 24:
            matched_records.append(val)
            rgb = hex_to_rgb(val["color"])
            if days_range == 1:
                nx, ny = HOUR_TO_5X5_COORD[hour_idx]
            else:
                nx = day_idx / max(1, days_range - 1)
                ny = (hour_idx - 1) / 23.0
            points.append((nx, ny, rgb))

    if not points:
        y_grid, x_grid = np.mgrid[0:canvas_size, 0:canvas_size] / float(canvas_size)
        r = (235 + 15 * x_grid).astype(np.uint8)
        g = (238 + 12 * y_grid).astype(np.uint8)
        b = (248 - 10 * x_grid).astype(np.uint8)
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

        dx = grid_x[:, :, None] - coords[None, None, :, 0]
        dy = grid_y[:, :, None] - coords[None, None, :, 1]
        dist_sq = dx**2 + dy**2 + 0.006
        weights = 1.0 / np.power(dist_sq, power / 2.0)

        weight_sum = np.sum(weights, axis=2, keepdims=True)
        norm_weights = weights / weight_sum

        blended_rgb = np.einsum("ijk,kl->ijl", norm_weights, colors)
        blended_rgb = np.clip(blended_rgb, 0, 255).astype(np.uint8)

        base_img = Image.fromarray(blended_rgb, mode="RGB")
        if blur_radius > 0:
            base_img = base_img.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    rgba_img = base_img.convert("RGBA")
    shape_mask = create_shape_mask(canvas_size, shape_name)
    rgba_img.putalpha(shape_mask)
    return rgba_img, matched_records


# ---------------------------------------------------------
# 4. 메인 UI 구성
# ---------------------------------------------------------
def main():
    init_session_state()

    st.markdown('<div class="main-title">🎨 감정 팔레트 (Emotion Palette)</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-title">매시간 기록한 감정과 색상이 좌표 위에서 어우러져 나만의 그라데이션 아트가 됩니다.</div>',
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.header("⚙️ 팔레트 설정")
        selected_range_label = st.selectbox(
            "📅 조회 및 팔레트 범위",
            list(RANGE_OPTIONS.keys()),
            index=0,
        )
        days_range = RANGE_OPTIONS[selected_range_label]

        selected_shape = st.selectbox(
            "✨ 팔레트 모형 선택",
            SHAPE_OPTIONS,
            index=0,
        )

        with st.expander("🎛️ 그라데이션 번짐 조절", expanded=False):
            spread_power = st.slider(
                "색상 경계 선명도 (낮을수록 넓게 퍼짐)",
                min_value=1.2,
                max_value=4.0,
                value=2.1,
                step=0.1,
            )
            blur_amount = st.slider(
                "수채화 블렌딩 강도",
                min_value=0,
                max_value=20,
                value=8,
                step=1,
            )

        st.divider()
        st.subheader("🧪 빠른 테스트 & 시연 도구")
        if st.button("✏️ 스케치 예시 재현 (빨강·파랑·주황·초록)", use_container_width=True):
            load_sketch_example()
            st.rerun()

        if st.button(f"🌈 {selected_range_label} 샘플 채우기", use_container_width=True):
            load_period_sample_data(days_range)
            st.rerun()

        if st.button("🗑️ 전체 기록 초기화", use_container_width=True):
            st.session_state.records = {}
            st.rerun()

        with st.expander("💾 기록 데이터 백업 / 불러오기"):
            json_str = json.dumps(st.session_state.records, ensure_ascii=False, indent=2)
            st.download_button(
                label="JSON 데이터 다운로드",
                data=json_str,
                file_name="emotion_records.json",
                mime="application/json",
                use_container_width=True,
            )
            uploaded_file = st.file_uploader("JSON 파일 불러오기", type=["json"])
            if uploaded_file is not None:
                try:
                    loaded = json.load(uploaded_file)
                    if isinstance(loaded, dict):
                        st.session_state.records = loaded
                        st.success("데이터를 성공적으로 불러왔습니다!")
                except Exception:
                    st.error("올바른 JSON 파일이 아닙니다.")

    left_col, right_col = st.columns([1.15, 1.0], gap="large")

    with left_col:
        st.subheader("1️⃣ 시간별 감정 및 색상 기록")

        if days_range > 1:
            day_idx = st.slider(
                "기록할 날짜 선택 (1일차 = 오늘)",
                min_value=1,
                max_value=days_range,
                value=min(st.session_state.selected_day + 1, days_range),
            ) - 1
            st.session_state.selected_day = day_idx
        else:
            st.session_state.selected_day = 0

        current_day = st.session_state.selected_day

        st.caption("아래 **5×5 시간표(1시~24시)**에서 기록할 시간 칸을 클릭하세요.")

        for row in GRID_5X5_LAYOUT:
            cols = st.columns(5, gap="small")
            for c_idx, hr in enumerate(row):
                with cols[c_idx]:
                    if hr is None:
                        st.markdown('<div class="center-badge">🎨 24H</div>', unsafe_allow_html=True)
                    else:
                        rec_key = f"{current_day}_{hr}"
                        rec = st.session_state.records.get(rec_key)
                        is_selected = st.session_state.selected_hour == hr
                        btn_label = f"{'👉 ' if is_selected else ''}{hr}시"
                        if st.button(btn_label, key=f"grid_btn_{current_day}_{hr}", use_container_width=True):
                            st.session_state.selected_hour = hr
                            st.rerun()

                        if rec:
                            bg = rec["color"]
                            fg = get_contrast_text_color(bg)
                            emo_short = rec["emotion"].split()[0]
                            st.markdown(
                                f'<div class="slot-preview" style="background:{bg}; color:{fg};">{emo_short}</div>',
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown(
                                '<div class="slot-preview" style="background:transparent; color:#999;">미기록</div>',
                                unsafe_allow_html=True,
                            )

        st.divider()

        target_hr = st.session_state.selected_hour
        target_key = f"{current_day}_{target_hr}"
        existing = st.session_state.records.get(target_key)

        day_label = f"{current_day + 1}일차 " if days_range > 1 else "오늘 "
        st.markdown(f"**✏️ {day_label}{target_hr}시 감정 입력**")

        in_col1, in_col2 = st.columns([1.4, 1.0])
        with in_col1:
            default_emo_idx = 0
            if existing and existing["emotion"] in PRESET_EMOTIONS:
                default_emo_idx = list(PRESET_EMOTIONS.keys()).index(existing["emotion"])
            chosen_emotion = st.selectbox(
                "대표 감정 선택",
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
                "세부 색상 선택 (컬러 피커)",
                value=initial_hex,
                key=f"cp_{target_key}_{chosen_emotion}",
            )

        note_text = st.text_input(
            "한 줄 메모 (선택 사항)",
            value=existing["note"] if existing else "",
            placeholder="이 시간의 기분이나 이유를 짧게 남겨보세요.",
        )

        act_col1, act_col2 = st.columns(2)
        with act_col1:
            if st.button("💾 이 시간 감정 저장하기", type="primary", use_container_width=True):
                st.session_state.records[target_key] = {
                    "emotion": chosen_emotion,
                    "color": chosen_color,
                    "note": note_text,
                }
                if target_hr < 24:
                    st.session_state.selected_hour = target_hr + 1
                st.rerun()

        with act_col2:
            if st.button("🧹 선택한 시간 기록 지우기", use_container_width=True):
                if target_key in st.session_state.records:
                    del st.session_state.records[target_key]
                    st.rerun()

    with right_col:
        st.subheader(f"2️⃣ 나만의 감정 팔레트 ({selected_range_label})")

        palette_img, matched_records = generate_emotion_palette(
            records=st.session_state.records,
            days_range=days_range,
            shape_name=selected_shape,
            power=spread_power,
            blur_radius=blur_amount,
            canvas_size=480,
        )

        st.image(
            palette_img,
            caption=f"모형: {selected_shape} | 기록된 시간: {len(matched_records)}개",
            use_container_width=True,
        )

        img_buffer = io.BytesIO()
        palette_img.save(img_buffer, format="PNG")
        st.download_button(
            label="🖼️ 감정 팔레트 이미지 저장 (PNG)",
            data=img_buffer.getvalue(),
            file_name=f"emotion_palette_{days_range}d.png",
            mime="image/png",
            use_container_width=True,
        )

        if matched_records:
            emotion_counts = {}
            for item in matched_records:
                emo = item["emotion"]
                emotion_counts[emo] = emotion_counts.get(emo, 0) + 1

            top_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0]
            total_slots = days_range * 24
            fill_rate = (len(matched_records) / total_slots) * 100

            st.markdown(
                f"""
                <div class="stat-card">
                    <div>📊 <b>기간 내 기록 수:</b> {len(matched_records)} / {total_slots}시간 ({fill_rate:.1f}%)</div>
                    <div style="margin-top:4px;">🏆 <b>가장 많이 느낀 감정:</b> {top_emotion} ({emotion_counts[top_emotion]}회)</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.info("아직 기록된 감정이 없습니다. 왼쪽 5×5 시간표에서 색상을 기록하거나 사이드바의 '스케치 예시 재현' 버튼을 눌러보세요!")


if __name__ == "__main__":
    main()
