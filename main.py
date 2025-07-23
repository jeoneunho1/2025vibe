import streamlit as st
import random

# --- 초기 메뉴 데이터 ---
default_menus = {
    "한식": ["김치찌개", "비빔밥", "불고기", "제육볶음", "냉면"],
    "중식": ["짜장면", "짬뽕", "탕수육", "마파두부"],
    "양식": ["파스타", "스테이크", "피자", "햄버거"],
    "일식": ["초밥", "라멘", "가츠동", "우동"]
}

# --- 세션 상태 초기화 ---
if "menus" not in st.session_state:
    st.session_state.menus = default_menus.copy()

if "history" not in st.session_state:
    st.session_state.history = []

# --- 앱 제목 ---
st.title("🍽️ 점심 메뉴 추천기")

# --- 카테고리 선택 ---
category = st.selectbox("카테고리를 선택하세요", list(st.session_state.menus.keys()))

# --- 메뉴 추천 기능 ---
st.subheader(f"👉 {category} 메뉴 추천")

if st.button("✨ 메뉴 추천 받기"):
    if st.session_state.menus[category]:
        selected = random.choice(st.session_state.menus[category])
        st.success(f"오늘의 추천 메뉴는 **{selected}** 입니다!")
        st.session_state.history.insert(0, f"[{category}] {selected}")
    else:
        st.warning("이 카테고리에 메뉴가 없습니다. 메뉴를 추가해보세요!")

# --- 메뉴 추가 ---
st.subheader("➕ 메뉴 추가")
new_menu = st.text_input("추가할 메뉴 이름")
if st.button("메뉴 추가"):
    if new_menu:
        if new_menu in st.session_state.menus[category]:
            st.warning("이미 존재하는 메뉴입니다.")
        else:
            st.session_state.menus[category].append(new_menu)
            st.success(f"{new_menu} 메뉴가 추가되었습니다.")
    else:
        st.error("메뉴 이름을 입력해주세요.")

# --- 메뉴 삭제 ---
st.subheader("🗑️ 메뉴 삭제")
if st.session_state.menus[category]:
    menu_to_delete = st.selectbox("삭제할 메뉴 선택", st.session_state.menus[category])
    if st.button("메뉴 삭제"):
        st.session_state.menus[category].remove(menu_to_delete)
        st.success(f"{menu_to_delete} 메뉴가 삭제되었습니다.")
else:
    st.info("삭제할 메뉴가 없습니다.")

# --- 추천 기록 보기 ---
st.subheader("📜 최근 추천 기록")
if st.session_state.history:
    st.write("\n".join(st.session_state.history[:10]))
else:
    st.info("추천 기록이 없습니다.")
