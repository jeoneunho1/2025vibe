import streamlit as st
from datetime import date

st.title("📅 입시 일정 관리")

event = st.text_input("일정 내용", "")
event_date = st.date_input("날짜 선택", date.today())

if st.button("➕ 일정 추가"):
    st.session_state.setdefault("schedules", []).append((event_date, event))
    st.success("✅ 일정이 추가되었습니다.")

if "schedules" in st.session_state:
    st.markdown("### 📌 등록된 일정")
    for d, e in sorted(st.session_state["schedules"]):
        st.markdown(f"- {d.strftime('%Y-%m-%d')} : **{e}**")