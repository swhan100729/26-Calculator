import streamlit as st
import pandas as pd
import plotly.express as px
import time
from datetime import datetime, date

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="학생용 학습 타이머", page_icon="⏱️", layout="wide")

# 2. 세션 상태(Session State) 초기화
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
if "elapsed_time" not in st.session_state:
    st.session_state.elapsed_time = 0
if "start_timestamp" not in st.session_state:
    st.session_state.start_timestamp = None
if "study_logs" not in st.session_state:
    st.session_state.study_logs = []
if "todos" not in st.session_state:
    st.session_state.todos = []

st.title("⏱️ 스마트 학생 학습 타이머 & 플래너")
st.caption("공부 시간을 과목별로 측정하고, 오늘 할 일을 체크하며 타임라인으로 시각화해보세요!")

# 화면 2열 레이아웃 구성
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📌 학습 타이머")
    
    # 과목 선택
    subject = st.selectbox(
        "공부할 과목을 선택하세요:",
        ["국어", "수학", "영어", "한국사", "탐구", "코딩", "기타"]
    )
    custom_subject = st.text_input("직접 과목 입력 (선택사항):")
    target_subject = custom_subject.strip() if custom_subject.strip() else subject

    # 시간 포맷 함수 (초 -> HH:MM:SS)
    def format_time(seconds):
        hrs = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hrs:02d}:{mins:02d}:{secs:02d}"

    # 타이머 시각화 디스플레이
    st.markdown(
        f"<div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center; margin: 15px 0;'>"
        f"<h1 style='color: #2E7D32; font-size: 50px; margin: 0;'>{format_time(st.session_state.elapsed_time)}</h1>"
        f"</div>",
        unsafe_allow_html=True
    )

    # 버튼 제어부 (시작/재개, 일시정지, 저장 및 초기화)
    btn_col1, btn_col2, btn_col3 = st.columns(3)

    if btn_col1.button("▶️ 시작 / 재개", use_container_width=True):
        if not st.session_state.timer_running:
            st.session_state.timer_running = True
            st.session_state.start_timestamp = time.time() - st.session_state.elapsed_time

    if btn_col2.button("⏸️ 일시정지", use_container_width=True):
        if st.session_state.timer_running:
            st.session_state.timer_running = False

    if btn_col3.button("⏹️ 기록 & 초기화", use_container_width=True):
        if st.session_state.elapsed_time > 0:
            mins = round(st.session_state.elapsed_time / 60, 1)
            st.session_state.study_logs.append({
                "과목": target_subject,
                "공부시간(분)": mins,
                "기록시간": datetime.now().strftime("%H:%M:%S"),
                "날짜": date.today().strftime("%Y-%m-%d")
            })
            st.success(f"'{target_subject}' 과목 {mins}분 학습 기록 저장 완료!")
        st.session_state.timer_running = False
        st.session_state.elapsed_time = 0
        st.session_state.start_timestamp = None
        st.rerun()

    # 타이머 실시간 갱신 로직
    if st.session_state.timer_running:
        st.session_state.elapsed_time = time.time() - st.session_state.start_timestamp
        time.sleep(0.1)
        st.rerun()

    st.markdown("---")
    st.subheader("✅ 오늘 할 일 (To-Do List)")
    
    # 할 일 추가 폼
    with st.form("todo_form", clear_on_submit=True):
        new_todo = st.text_input("새로운 할 일을 입력하세요:")
        submitted = st.form_submit_button("추가")
        if submitted and new_todo.strip():
            st.session_state.todos.append({"task": new_todo.strip(), "done": False})
            st.rerun()

    # 할 일 목록 출력 및 체크박스 처리
    if st.session_state.todos:
        for i, todo in enumerate(st.session_state.todos):
            checked = st.checkbox(todo["task"], value=todo["done"], key=f"todo_{i}")
            st.session_state.todos[i]["done"] = checked
    else:
        st.info("등록된 할 일이 없습니다. 오늘 할 일을 입력해보세요!")

with col2:
    st.subheader("📊 과목별 기록 & 타임라인 시각화")
    
    if st.session_state.study_logs:
        df = pd.DataFrame(st.session_state.study_logs)
        
        # 총 공부 시간 요약
        total_mins = df["공부시간(분)"].sum()
        st.metric(label="오늘 총 공부 시간", value=f"{total_mins:.1f} 분", delta=f"{total_mins/60:.2f} 시간")

        # 1. 과목별 합계 막대 그래프
        subject_sum = df.groupby("과목")["공부시간(분)"].sum().reset_index()
        fig_bar = px.bar(
            subject_sum, 
            x="과목", 
            y="공부시간(분)", 
            color="과목",
            title="과목별 누적 학습 시간 (분)",
            text_auto=True
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # 2. 타임라인(세션별 흐름) 그래프
        fig_timeline = px.line(
            df, 
            x="기록시간", 
            y="공부시간(분)", 
            color="과목", 
            markers=True,
            title="학습 진행 타임라인"
        )
        st.plotly_chart(fig_timeline, use_container_width=True)

        # 세부 데이터 테이블
        with st.expander("📝 상세 학습 기록 보기"):
            st.dataframe(df, use_container_width=True)
    else:
        st.info("아직 저장된 학습 기록이 없습니다. 타이머로 공부 시간을 측정한 후 기록해 보세요!")
