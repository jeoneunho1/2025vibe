import streamlit as st

grade_score = {"1등급": 1.0, "2등급": 2.0, "3등급": 3.0, "4등급": 4.0, "5등급": 5.0}
target_level = {
    "의대/치대/한의대/SKY": 1.1,
    "서성한": 1.2,
    "중경외시/건동홍/시립대": 1.3,
    "숙명여대/세종대/가천대": 1.4,
    "단국대/아주대/국민대 등": 1.55,
    "지방 국립대": 2.5,
    "전문대": 3.5
}
def predict_university(avg):
    for group, threshold in target_level.items():
        if avg <= threshold:
            return group
    return "전문대"

st.title("📚 내신 성적 입력 및 분석")

if "subjects" not in st.session_state:
    st.session_state.subjects = [
        {"name": "국어", "unit": 4, "grade": "2등급"},
        {"name": "영어", "unit": 4, "grade": "2등급"},
        {"name": "수학", "unit": 4, "grade": "2등급"},
        {"name": "사회", "unit": 3, "grade": "2등급"},
        {"name": "과학", "unit": 3, "grade": "2등급"},
        {"name": "한국사", "unit": 3, "grade": "2등급"},
    ]

st.markdown("### ➕ 선택 과목 추가")
with st.form("add_subject_form"):
    name = st.text_input("과목명 (예: 정보)", key="add_name")
    unit = st.number_input("단위수", 1, 10, value=3, key="add_unit")
    grade = st.selectbox("등급", list(grade_score.keys()), key="add_grade")
    submit = st.form_submit_button("➕ 추가")
    if submit and name:
        st.session_state.subjects.append({"name": name, "unit": unit, "grade": grade})
        st.success(f"{name} 과목이 추가되었습니다.")

# 과목별 입력
for i, subj in enumerate(st.session_state.subjects):
    col1, col2, col3 = st.columns([3, 2, 2])
    subj["name"] = col1.text_input(f"과목명 {i+1}", subj["name"], key=f"name_{i}")
    subj["unit"] = col2.number_input(f"단위수 {i+1}", 1, 10, subj["unit"], key=f"unit_{i}")
    subj["grade"] = col3.selectbox(f"등급 {i+1}", list(grade_score.keys()), key=f"grade_{i}", index=list(grade_score).index(subj["grade"]))

# 분석
total_score = sum(grade_score[s["grade"]] * s["unit"] for s in st.session_state.subjects)
total_units = sum(s["unit"] for s in st.session_state.subjects)
avg_grade = round(total_score / total_units, 2)
group = predict_university(avg_grade)
st.success(f"📌 내신 평균 등급: **{avg_grade}**, 예측 대학군: **{group}**")