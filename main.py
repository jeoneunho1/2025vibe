import streamlit as st
import random

# 점심 메뉴 리스트
menu_list = [
    "김치찌개",
    "된장찌개",
    "비빔밥",
    "불고기",
    "돈까스",
    "제육볶음",
    "냉면",
    "칼국수",
    "김밥",
    "떡볶이",
    "쌀국수",
    "햄버거"
]

# 앱 제목
st.title("🍱 오늘 뭐 먹지?")

# 메뉴 설명
st.write("점심 메뉴가 고민될 때, 버튼을 눌러 추천을 받아보세요!")

# 버튼을 눌렀을 때 랜덤 추천
if st.button("메뉴 추천 받기"):
    selected_menu = random.choice(menu_list)
    st.success(f"👉 오늘의 추천 메뉴는 **{selected_menu}** 입니다!")
