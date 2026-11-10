import streamlit as st
import time

# -----------------------------------------------------------------------------
# 1. 페이지 기본 설정 및 세션 상태 초기화
# -----------------------------------------------------------------------------
st.set_page_config(page_title="학생용 학습 타이머", page_icon="⏱️", layout="centered")

# 앱 상태(데이터) 저장 공간 초기화
if "records" not in st.session_state:
    st.session_state.records = {}  # 과목별 누적 시간 저장 (초 단위)
if "is_running" not in st.session_state:
    st.session_state.is_running = False  # 타이머 실행 여부
if "start_time" not in st.session_state:
    st.session_state.start_time = 0.0  # 현재 회차 시작 시각
if "current_subject" not in st.session_state:
    st.session_state.current_subject = "국어"

st.title("⏱️ 학생용 학습 타이머")
st.write("과목별로 공부 시간을 측정하고 효율적으로 관리해보세요!")

# -----------------------------------------------------------------------------
# 2. 과목 선택 영역
# -----------------------------------------------------------------------------
st.subheader("📚 1. 과목 선택")
preset_subjects = ["국어", "수학", "영어", "한국사", "탐구", "직접 입력"]
selected_option = st.selectbox("공부할 과목을 선택하세요:", preset_subjects)

if selected_option == "직접 입력":
    subject_name = st.text_input("과목명을 입력하세요:", value="자율학습")
else:
    subject_name = selected_option

# 선택 과목이 변경되면 진행 중인 타이머 정지
if subject_name != st.session_state.current_subject:
    st.session_state.is_running = False
    st.session_state.current_subject = subject_name

# 해당 과목의 기록이 없으면 0초로 초기화
if subject_name not in st.session_state.records:
    st.session_state.records[subject_name] = 0.0

# -----------------------------------------------------------------------------
# 3. 타이머 시간 계산 및 표시
# -----------------------------------------------------------------------------
base_time = st.session_state.records[subject_name]

# 타이머 동작 중일 때 현재 구간 시간 더하기
if st.session_state.is_running:
    elapsed_current = time.time() - st.session_state.start_time
else:
    elapsed_current = 0.0

total_seconds = int(base_time + elapsed_current)

# 초 단위 데이터를 HH:MM:SS 형식으로 변환
hours = total_seconds // 3600
minutes = (total_seconds % 3600) // 60
seconds = total_seconds % 60
formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

st.subheader(f"🎯 현재 과목: {subject_name}")
st.markdown(
    f"<h1 style='text-align: center; color: #2E86C1; font-size: 64px;'>{formatted_time}</h1>",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 4. 제어 버튼 (시작 / 일시정지 / 초기화)
# -----------------------------------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("▶️ 시작", use_container_width=True, disabled=st.session_state.is_running):
        st.session_state.is_running = True
        st.session_state.start_time = time.time()
        st.rerun()

with col2:
    if st.button("⏸️ 일시정지", use_container_width=True, disabled=not st.session_state.is_running):
        # 이번 구간 학습 시간을 누적 기록에 반영
        added_time = time.time() - st.session_state.start_time
        st.session_state.records[subject_name] += added_time
        st.session_state.is_running = False
        st.rerun()

with col3:
    if st.button("🔄 초기화", use_container_width=True):
        st.session_state.is_running = False
        st.session_state.records[subject_name] = 0.0
        st.rerun()

# 타이머 실행 중일 경우 1초마다 화면 자동 갱신
if st.session_state.is_running:
    time.sleep(1)
    st.rerun()

# -----------------------------------------------------------------------------
# 5. 과목별 시간 기록표 표시
# -----------------------------------------------------------------------------
st.divider()
st.subheader("📊 과목별 누적 공부 시간")

has_records = any(sec > 0 for sec in st.session_state.records.values())

if has_records:
    for subj, sec in st.session_state.records.items():
        if sec > 0:
            tot_sec = int(sec)
            h = tot_sec // 3600
            m = (tot_sec % 3600) // 60
            s = tot_sec % 60
            st.write(f"- **{subj}**: `{h:02d}시간 {m:02d}분 {s:02d}초`")
else:
    st.info("아직 기록된 공부 시간이 없습니다. [시작] 버튼을 눌러 열공을 시작해보세요!")
