import streamlit as st
import random
import datetime

# --- 초기 다양한 메뉴 데이터 ---
default_menus = {
    "한식": [
        {"name": "김치찌개", "kcal": 230, "carbs": 12, "protein": 15, "fat": 10},
        {"name": "된장찌개", "kcal": 200, "carbs": 10, "protein": 10, "fat": 8},
        {"name": "비빔밥", "kcal": 550, "carbs": 80, "protein": 18, "fat": 12},
        {"name": "불고기", "kcal": 420, "carbs": 20, "protein": 25, "fat": 22},
        {"name": "제육볶음", "kcal": 510, "carbs": 18, "protein": 27, "fat": 30},
        {"name": "냉면", "kcal": 370, "carbs": 60, "protein": 10, "fat": 5},
        {"name": "갈비탕", "kcal": 400, "carbs": 5, "protein": 25, "fat": 30},
        {"name": "콩나물국밥", "kcal": 350, "carbs": 45, "protein": 20, "fat": 8},
        {"name": "순두부찌개", "kcal": 280, "carbs": 8, "protein": 14, "fat": 18},
        {"name": "오징어볶음", "kcal": 320, "carbs": 15, "protein": 25, "fat": 14},
        {"name": "닭갈비", "kcal": 480, "carbs": 20, "protein": 35, "fat": 22},
        {"name": "떡갈비", "kcal": 450, "carbs": 25, "protein": 20, "fat": 28},
        {"name": "감자탕", "kcal": 520, "carbs": 20, "protein": 35, "fat": 30}
    ],
    "중식": [
        {"name": "짜장면", "kcal": 520, "carbs": 85, "protein": 12, "fat": 15},
        {"name": "짬뽕", "kcal": 480, "carbs": 60, "protein": 20, "fat": 14},
        {"name": "탕수육", "kcal": 600, "carbs": 50, "protein": 20, "fat": 30},
        {"name": "마파두부", "kcal": 350, "carbs": 10, "protein": 18, "fat": 25},
        {"name": "깐풍기", "kcal": 550, "carbs": 30, "protein": 25, "fat": 32},
        {"name": "양장피", "kcal": 420, "carbs": 40, "protein": 15, "fat": 22},
        {"name": "볶음밥", "kcal": 530, "carbs": 70, "protein": 15, "fat": 20}
    ],
    "양식": [
        {"name": "스테이크", "kcal": 600, "carbs": 10, "protein": 40, "fat": 35},
        {"name": "샐러드", "kcal": 200, "carbs": 10, "protein": 5, "fat": 12},
        {"name": "파스타", "kcal": 500, "carbs": 65, "protein": 15, "fat": 18},
        {"name": "피자", "kcal": 700, "carbs": 70, "protein": 20, "fat": 35},
        {"name": "햄버거", "kcal": 650, "carbs": 50, "protein": 25, "fat": 40},
        {"name": "리조또", "kcal": 480, "carbs": 60, "protein": 10, "fat": 20},
        {"name": "크림스프", "kcal": 300, "carbs": 20, "protein": 5, "fat": 22}
    ],
    "일식": [
        {"name": "초밥", "kcal": 450, "carbs": 70, "protein": 18, "fat": 10},
        {"name": "라멘", "kcal": 550, "carbs": 60, "protein": 20, "fat": 25},
        {"name": "가츠동", "kcal": 600, "carbs": 70, "protein": 25, "fat": 28},
        {"name": "우동", "kcal": 430, "carbs": 65, "protein": 10, "fat": 12},
        {"name": "규동", "kcal": 500, "carbs": 65, "protein": 22, "fat": 20},
        {"name": "돈카츠", "kcal": 550, "carbs": 35, "protein": 20, "fat": 35}
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

# --- 요일 계산 ---
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
st.title("🍽️ 오늘 뭐 먹지?")
st.write(f"📆 오늘은 **{today_kor}**, 추천 테마에 맞는 점심을 골라드릴게요!")

# --- 카테고리 선택 ---
category = st.selectbox("🍱 카테고리를 선택하세요", list(st.session_state.menus.keys()))

# --- 추천 포맷 함수 ---
def format_menu(menu):
    return f"{menu['name']} ({menu['kcal']} kcal, 탄:{menu['carbs']}g, 단:{menu['protein']}g, 지:{menu['fat']}g)"

# --- 메뉴 추천 ---
st.subheader("✨ 오늘의 점심 추천")
if st.button("메뉴 추천 받기"):
    menus = st.session_state.menus[category]

    if theme:
        themed = [m for m in menus if any(k in m["name"] for k in theme)]
    else:
        themed = []

    if themed:
        selected = random.choice(themed)
        st.success(f"✅ 테마 추천 메뉴: **{format_menu(selected)}**")
    elif menus:
        selected = random.choice(menus)
        st.success(f"🎲 랜덤 추천 메뉴: **{format_menu(selected)}**")
    else:
        st.warning("추천할 메뉴가 없습니다.")
        selected = None

    if selected:
        st.session_state.history.insert(0, f"[{today_kor} / {category}] {format_menu(selected)}")

# --- 메뉴 추가 ---
st.subheader("➕ 메뉴 추가")
with st.form("add_menu_form"):
    name = st.text_input("메뉴 이름")
    kcal = st.number_input("칼로리 (kcal)", min_value=0, value=0)
    carbs = st.number_input("탄수화물 (g)", min_value=0, value=0)
    protein = st.number_input("단백질 (g)", min_value=0, value=0)
    fat = st.number_input("지방 (g)", min_value=0, value=0)
    add = st.form_submit_button("추가")

if add:
    if name:
        if any(m['name'] == name for m in st.session_state.menus[category]):
            st.warning("이미 존재하는 메뉴입니다.")
        else:
            st.session_state.menus[category].append({
                "name": name, "kcal": kcal, "carbs": carbs, "protein": protein, "fat": fat
            })
            st.success(f"{name} 메뉴가 추가되었습니다.")
    else:
        st.error("메뉴 이름을 입력해주세요.")

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

# --- 추천 기록 보기 ---
st.subheader("📜 최근 추천 기록")
if st.session_state.history:
    for record in st.session_state.history[:10]:
        st.write(record)
else:
    st.info("아직 추천 기록이 없습니다.")
