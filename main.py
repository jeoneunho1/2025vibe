import streamlit as st

st.title("🎓 2028 내신 성취도 분석기 (절대평가 5등급제 기반)")
st.caption("과목 직접 입력 + 단위수 설정 → 평균 등급 기반 대학군 예측 & 보완 전략 제공")

# 등급 점수 매핑
grade_score = {
    "1등급": 1.0,
    "2등급": 2.0,
    "3등급": 3.0,
    "4등급": 4.0,
    "5등급": 5.0
}

st.subheader("📚 과목 추가 및 설정")

# 세션 상태로 과목 리스트 관리
if "subjects" not in st.session_state:
    st.session_state.subjects = [
        {"name": "국어", "unit": 4, "grade": "2등급"},
        {"name": "영어", "unit": 4, "grade": "2등급"},
        {"name": "수학", "unit": 4, "grade": "2등급"},
    ]

# 과목 추가
with st.form("add_subject_form"):
    new_name = st.text_input("과목명", "")
    new_unit = st.number_input("단위수", min_value=1, max_value=10, value=3)
    new_grade = st.selectbox("등급", list(grade_score.keys()))
    submitted = st.form_submit_button("➕ 과목 추가")
    if submitted and new_name:
        st.session_state.subjects.append({
            "name": new_name,
            "unit": new_unit,
            "grade": new_grade
        })
        st.success(f"'{new_name}' 과목이 추가되었습니다.")

# 과목 리스트 표시 및 삭제 기능
st.markdown("### 현재 입력된 과목들")

remove_indices = []
total_score = 0
total_units = 0
subject_grades = {}

for i, subj in enumerate(st.session_state.subjects):
    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
    with col1:
        subj["name"] = st.text_input(f"과목명 {i+1}", value=subj["name"], key=f"name_{i}")
    with col2:
        subj["unit"] = st.number_input(f"단위수 {i+1}", min_value=1, max_value=10, value=subj["unit"], key=f"unit_{i}")
    with col3:
        subj["grade"] = st.selectbox(f"등급 {i+1}", options=list(grade_score.keys()), index=list(grade_score.keys()).index(subj["grade"]), key=f"grade_{i}")
    with col4:
        if st.button("🗑️ 삭제", key=f"remove_{i}"):
            remove_indices.append(i)

# 삭제 요청 처리
for i in sorted(remove_indices, reverse=True):
    del st.session_state.subjects[i]

# 평균 등급 계산
for subj in st.session_state.subjects:
    score = grade_score[subj["grade"]]
    total_score += score * subj["unit"]
    total_units += subj["unit"]
    subject_grades[subj["name"]] = score

if total_units == 0:
    st.warning("과목을 추가하고 단위수를 입력해주세요.")
else:
    avg_grade = round(total_score / total_units, 2)

    st.subheader("📊 내신 평균 등급 결과")
    st.write(f"📌 **가중 평균 등급**: {avg_grade} 등급")

    # 대학 예측
    def predict_university(avg):
        if avg <= 1.10:
            return "🏆 의대, 치대, 한의대, 약대, 수의대, SKY(서울대/연세대/고려대)"
        elif avg <= 1.20:
            return "🥇 서강대, 성균관대, 한양대(서울), 이화여대"
        elif avg <= 1.30:
            return "🎯 중경외시, 건국대(서울), 동국대, 홍익대, 서울시립대"
        elif avg <= 1.40:
            return "✅ 숙명여대, 서울여대, 세종대, 명지대, 가천대"
        elif avg <= 1.55:
            return "💡 숭실대, 단국대, 아주대, 광운대, 국민대, 상명대"
        elif avg <= 1.80:
            return "📘 서울과기대, 덕성여대, 한성대, 한신대, 서경대"
        elif avg <= 2.10:
            return "🔍 인하대, 인천대, 경기대, 가톨릭대 등 수도권 적성전형/논술 대학"
        elif avg <= 2.50:
            return "🏫 전북대, 전남대, 충남대, 경북대, 부경대 등 지방 거점 국립대"
        elif avg <= 3.20:
            return "🪴 대구대, 한남대, 우석대, 창원대, 계명대 등 지방 사립대"
        else:
            return "📉 전문대학 / 실기·특기자 / 직업계고 전형 추천"

    st.subheader("🎓 예상 지원 가능 대학군")
    st.success(f"👉 {predict_university(avg_grade)}")

    # 보완 전략 제안
    st.subheader("💡 보완 전략: 개선하면 효과 큰 과목")
    weak_subjects = sorted(subject_grades.items(), key=lambda x: -x[1])[:2]

    for subj, score in weak_subjects:
        if score > 1.0:
            st.info(f"📌 **{subj}** 현재 {score}등급 → 성적 향상 시 전체 평균 등급 개선 효과 큼!")

st.markdown("---")
st.caption("🔍 본 분석은 2028 대입 절대평가 5등급제 + 단위수 기반 내신 가중 평균을 기준으로 합니다.")
