import streamlit as st
import random
import datetime

# --- 초기 메뉴 데이터 ---
default_menus = {
    "한식": [
        {"name": "김치찌개", "kcal": 230, "carbs": 12, "protein": 15, "fat": 10},
        {"name": "비빔밥", "kcal": 550, "carbs": 80, "protein": 18, "fat": 12},
        {"name": "불고기", "kcal": 420, "carbs": 20, "protein": 25, "fat": 22}
    ],
    "양식": [
        {"name": "스테이크", "kcal": 600, "carbs": 10, "protein": 40, "fat": 35},
        {"name": "샐러드", "kcal": 200, "carbs": 10, "protein": 5, "fat": 12}
    ]
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

# --- 세션 초기화 ---
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

# --- UI: 앱 제목 ---
st.title("🍱 건강한 점심 메뉴 추천기")
st.write(f"📅 오늘은 **{today_kor}**, 건강까지 생각한 점심을 추천해드릴게요!")

# --- 카테고리 선택 ---
category = st.selectbox("카테고리를 선택하세요", list(st.session_state.menus.keys()))

# --- 추천 버튼 ---
st.subheader(f"👉 {category} 메뉴 추천")

def format_menu_info(menu):
    return f"{menu['name']} ({menu['kcal']} kcal, 탄:{menu['carbs']}g, 단:{menu['protein']}g, 지:{menu['fat']}g)"

if st.button("✨ 오늘 메뉴 추천 받기"):
    menus = st.session_state.menus[category]
    
    themed = [m for m in menus if any(k in m['name'] for k in theme)]

    if themed:
        selected = random.choice(themed)
        st.success(f"오늘의 추천 메뉴는 👉 **{format_menu_info(selected)}** 🎉")
    elif menus:
        selected = random.choice(menus)
        st.success(f"테마 메뉴는 없지만 랜덤 추천! 👉 **{format_menu_info(selected)}**")
    else:
        st.warning("이 카테고리에 메뉴가 없습니다. 메뉴를 추가해보세요.")
        selected = None

    if selected:
        st.session_state.history.insert(0, f"[{today_kor} / {category}] {format_menu_info(selected)}")

# --- 메뉴 추가 ---
st.subheader("➕ 메뉴 추가")
with st.form("add_menu"):
    name = st.text_input("메뉴 이름", key="name")
    kcal = st.number_input("칼로리 (kcal)", min_value=0, value=0)
    carbs = st.number_input("탄수화물 (g)", min_value=0, value=0)
    protein = st.number_input("단백질 (g)", min_value=0, value=0)
    fat = st.number_input("지방 (g)", min_value=0, value=0)
    submitted = st.form_submit_button("메뉴 추가")

if submitted:
    if name:
        if any(m['name'] == name for m in st.session_state.menus[category]):
            st.warning("이미 존재하는 메뉴입니다.")
        else:
            st.session_state.menus[category].append({
                "name": name, "kcal": kcal, "carbs": carbs, "protein": protein, "fat": fat
            })
            st.success(f"{name} 메뉴가 추가되었습니다!")
    else:
        st.error("메뉴 이름은 필수입니다.")

# --- 메뉴 삭제 ---
st.subheader("🗑️ 메뉴 삭제")
if st.session_state.menus[category]:
    to_delete = st.selectbox(
        "삭제할 메뉴 선택",
        st.session_state.menus[category],
        format_func=lambda m: m["name"]
    )
    if st.button("삭제"):
        st.session_state.menus[category].remove(to_delete)
        st.success(f"{to_delete['name']} 메뉴가 삭제되었습니다.")
else:
    st.info("삭제할 메뉴가 없습니다.")

# --- 추천 기록 ---
st.subheader("📜 최근 추천 기록")
if st.session_state.history:
    st.write("\n".join(st.session_state.history[:10]))
else:
    st.info("추천 기록이 없습니다.")
