import streamlit as st
import random
import time

# 음식 옵션 리스트
food_options = [
    "김치찌개",
    "비빔밥",
    "짜장면",
    "햄버거",
    "샐러드",
    "돈까스",
    "초밥",
    "라면",
    "불고기",
    "제육볶음"
]

st.set_page_config(page_title="점심메뉴 룰렛", page_icon="🎯")
st.title("🎯 점심메뉴 룰렛")
st.markdown("점심 메뉴가 고민될 땐 룰렛을 돌려보세요!")

if "spinning" not in st.session_state:
    st.session_state.spinning = False
if "selected" not in st.session_state:
    st.session_state.selected = ""

def spin_roulette():
    st.session_state.spinning = True
    st.session_state.selected = ""
    with st.spinner("룰렛을 돌리는 중..."):
        time.sleep(2)
        st.session_state.selected = random.choice(food_options)
    st.session_state.spinning = False

st.button("룰렛 돌리기", on_click=spin_roulette, disabled=st.session_state.spinning)

if st.session_state.selected:
    st.success(f"오늘의 점심 메뉴는: **{st.session_state.selected}**!")
else:
    st.info("아직 메뉴가 선택되지 않았어요. 버튼을 눌러 돌려보세요!")
