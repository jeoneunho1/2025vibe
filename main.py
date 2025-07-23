import streamlit as st
import random
import datetime

# --- 초기 메뉴 데이터 ---
default_menus = {
    "한식": ["김치찌개", "비빔밥", "불고기", "제육볶음", "냉면", "된장찌개", "콩나물국밥", "갈비탕"],
    "중식": ["짜장면", "짬뽕", "탕수육", "마파두부", "꿔바로우"],
    "양식": ["파스타", "스테이크", "피자", "햄버거", "샐러드"],
    "일식": ["초밥", "라멘", "가츠동", "우동", "규동"]
}

# --- 요일별 테마 키워드 ---
theme_keywords = {
    "월요일": ["국밥", "된장", "찌개", "죽"],
    "화요일": ["불고기", "제육", "스테이크", "고기"],
    "수요일": ["국", "탕", "라멘", "우동", "짬뽕"],
    "목요일": ["샐러드", "비빔밥", "냉면", "가벼운"],
    "금요일": ["피자", "초밥", "스페셜", "햄버거", "탕수육"],
    "토요일": [],
    "일요일": []
}

# --- 세션 상태 초기화 ---
if "menus" not in st.session_state:
    st.session_state.menus = default_menus.copy()

if "history" not in st.session_state:
    st.session_state.history = []

# --- 오늘 요일 계산 ---
today = datetime.datetime.today().strftime('%A')
weekday_kor = {
    'Monday': '월요일',
    'Tuesday': '화요일',
    'Wednesday': '수요일',
    'Thursday': '목요일',
    'Friday': '금요일',
    'Saturday': '토요일',
    'Sunday': '일요일'
}
today_kor = weekday_kor[today]
theme = theme_keywords[today_kor]

# --- 앱 제목 ---
st.title("🍽️ 점심 메뉴 추천기")
st.write(f"🗓️ 오늘은 **{today_kor}**이에요. 추천 테마에 맞춰 골라드릴게요!")

# --- 카테고리 선택 ---
category = st.selectbox("카테고리를 선택하세요", list(st.session_state.menus.keys()))

# --- 추천 기능 ---
st.subheader(f"👉 {category} 메뉴 추천")

if st.button("✨ 오늘 메뉴 추천 받기"):
    menus = st.session_state.menus[category]
    
    # 요일 테마 우선 필터
    themed_menus = [m for m in menus if any(k in m for k in theme)]
    
    if themed_menus:
        selected = random.choice(themed_menus)
        st.success(f"오늘은 {today_kor} 테마! 추천 메뉴는 **{selected}** 입니다 🎉")
    elif menus:
        selected = random.choice(menus)
        st.success(f"테마에 맞는 메뉴는 없지만, 랜덤 추천! 👉 **{selected}**")
    else:
        st.warning("이 카테고리에 메뉴가 없습니다. 메뉴를 추가해보세요.")
        selected = None

    if selected:
        st.session_state.history.insert(0, f"[{today_kor} / {category}] {selected}")

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
