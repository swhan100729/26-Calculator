import streamlit as st
import pandas as pd
import plotly.express as px
import time
from datetime import datetime, date

# 1. 페이지 기본 설정
st.set_page_config(page_title="학생용 학습 플래너 앱", page_icon="⏱️", layout="wide")

# 2. 세션 상태(Session State) 초기화 (앱 전체 공유)
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
if "elapsed_time" not in st.session_state:
    st.session_state.elapsed_time = 0
if "start_timestamp" not in st.session_state:
    st.session_state.start_timestamp = None
if "study_logs" not in st.session_state:
    st.session_state.study_logs = []
if "todos" not in st.session_state:
    # 각 항목: {"subject": 과목, "task": 할일, "done": 완료여부}
    st.session_state.todos = []

# 3. 사이드바 메뉴 구성
st.sidebar.title("📌 메뉴 목록")
menu = st.sidebar.radio(
    "이동할 메뉴를 선택하세요:",
    ["⏱️ 공부 타이머", "✅ 오늘 할일", "📝 공부 회고"]
)

# ---------------------------------------------------------
# 메뉴 1: 공부 타이머
# ---------------------------------------------------------
if menu == "⏱️ 공부 타이머":
    st.title("⏱️ 스마트 학생 학습 타이머")
    st.caption("공부 시간을 과목별로 측정하고, 진행 상황을 실시간으로 확인해보세요!")

    # 화면 2열 레이아웃
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
        st.subheader("✅ 오늘 할 일 목록 요약")
        
        if st.session_state.todos:
            done_count = sum(1 for t in st.session_state.todos if t["done"])
            st.progress(done_count / len(st.session_state.todos))
            st.write(f"총 {len(st.session_state.todos)}개 중 {done_count}개 완료")
        else:
            st.info("등록된 할 일이 없습니다. '✅ 오늘 할일' 메뉴에서 등록해보세요!")

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

            # 2. 타임라인 그래프
            fig_timeline = px.line(
                df, 
                x="기록시간", 
                y="공부시간(분)", 
                color="과목", 
                markers=True,
                title="학습 진행 타임라인"
            )
            st.plotly_chart(fig_timeline, use_container_width=True)

            with st.expander("📝 상세 학습 기록 보기"):
                st.dataframe(df, use_container_width=True)
        else:
            st.info("아직 저장된 학습 기록이 없습니다. 타이머로 공부 시간을 측정한 후 기록해 보세요!")

# ---------------------------------------------------------
# 메뉴 2: 오늘 할일 (과목 + 할일 입력 및 완료 취소선 체크)
# ---------------------------------------------------------
elif menu == "✅ 오늘 할일":
    st.title("✅ 오늘 할일 관리")
    st.caption("과목별로 할 일을 등록하고, 완료한 항목을 체크하여 목표를 달성해보세요!")

    # 1. 할 일 추가 입력 폼
    with st.form("add_todo_form", clear_on_submit=True):
        col_sub, col_task, col_btn = st.columns([1, 2, 0.8])
        
        with col_sub:
            todo_subject = st.selectbox(
                "과목 선택",
                ["국어", "수학", "영어", "한국사", "탐구", "코딩", "기타"],
                key="todo_sub_select"
            )
        with col_task:
            todo_task = st.text_input("할 일 내용 입력", placeholder="예: 개념원리 30페이지 풀기")
        
        with col_btn:
            st.write("") # 버튼 위치 맞춤용 공백
            st.write("")
            add_submitted = st.form_submit_button("➕ 추가", use_container_width=True)

        if add_submitted:
            if todo_task.strip():
                st.session_state.todos.append({
                    "subject": todo_subject,
                    "task": todo_task.strip(),
                    "done": False
                })
                st.success(f"[{todo_subject}] {todo_task} 항목이 추가되었습니다!")
                st.rerun()
            else:
                st.warning("할 일 내용을 입력해주세요.")

    st.markdown("---")
    st.subheader("📋 할 일 목록")

    # 2. 할 일 목록 출력 및 체크박스/취소선 처리
    if st.session_state.todos:
        # 달성률 계산 및 프로그레스 바 표시
        total_todos = len(st.session_state.todos)
        completed_todos = sum(1 for t in st.session_state.todos if t["done"])
        progress_ratio = completed_todos / total_todos
        
        st.write(f"**진행 상황**: {completed_todos} / {total_todos}개 완료 ({int(progress_ratio * 100)}%)")
        st.progress(progress_ratio)
        st.write("")

        # 목록 항목 렌더링
        for i, item in enumerate(st.session_state.todos):
            c_check, c_text, c_del = st.columns([0.08, 0.82, 0.1])
            
            with c_check:
                checked = st.checkbox(
                    "", 
                    value=item["done"], 
                    key=f"chk_{i}", 
                    label_visibility="collapsed"
                )
                st.session_state.todos[i]["done"] = checked

            with c_text:
                label_text = f"**[{item['subject']}]** {item['task']}"
                if checked:
                    # 체크되었을 시 취소선(~~) 적용
                    st.markdown(f"~~{label_text}~~", unsafe_allow_html=True)
                else:
                    st.markdown(label_text)

            with c_del:
                if st.button("🗑️", key=f"del_{i}", help="삭제"):
                    st.session_state.todos.pop(i)
                    st.rerun()

            # 체크 상태 변경 시 즉시 화면 갱신이 필요할 경우를 위한 갱신
            if checked != item["done"]:
                st.rerun()
    else:
        st.info("아직 등록된 할 일이 없습니다. 상단 폼에서 과목과 할 일을 입력하고 추가해보세요!")

# ---------------------------------------------------------
# 메뉴 3: 공부 회고
# ---------------------------------------------------------
elif menu == "📝 공부 회고":
    st.title("📝 공부 회고")
    st.caption("오늘의 학습 과정과 잘한 점, 아쉬운 점을 기록하고 일기 형태로 남기는 공간입니다.")
    st.info("💡 이 페이지는 준비 중입니다. 향후 일일 회고 작성 및 주간 분석 기능이 추가될 예정입니다!")
