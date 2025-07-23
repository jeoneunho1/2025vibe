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

st.title("📈 성적 향상 시뮬레이션")

if "subjects" not in st.session_state or len(st.session_state.subjects) == 0:
    st.warning("📌 내신 과목을 먼저 입력해주세요 (내신 분석 페이지)")
else:
    target_subj = st.selectbox("향상할 과목", [s["name"] for s in st.session_state.subjects])
    target_grade = st.selectbox("목표 등급", list(grade_score.keys()))

    total_units = sum(s["unit"] for s in st.session_state.subjects)
    sim_score = 0
    for subj in st.session_state.subjects:
        score = grade_score[target_grade] if subj["name"] == target_subj else grade_score[subj["grade"]]
        sim_score += score * subj["unit"]
    sim_avg = round(sim_score / total_units, 2)
    sim_group = predict_university(sim_avg)

    st.markdown(f"✅ `{target_subj}`을 **{target_grade}**로 올리면 → 평균: **{sim_avg}**, 예상 대학군: **{sim_group}**")