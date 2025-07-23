import streamlit as st
import pandas as pd

st.set_page_config(page_title="2028 내신 분석기", layout="wide")

st.title("🎓 2028 내신 성취도 분석기 (절대평가 5등급제 기반)")
st.caption("주요 과목 + 단위수 반영 평균 등급 → 대학 예측 & 시뮬레이션 + 전략 조언 + 대학별 내신 링크")

# 등급 점수 매핑
grade_score = {
    "1등급": 1.0,
    "2등급": 2.0,
    "3등급": 3.0,
    "4등급": 4.0,
    "5등급": 5.0
}

# 대학군 → 대표 대학명 + 어디가 unvCd
univ_links = {
    "의대/치대/한의대/SKY": [("서울대", "0000001"), ("연세대", "0000011"), ("고려대", "0000015")],
    "서성한": [("서강대", "0000030"), ("성균관대", "0000025"), ("한양대", "0000035")],
    "중경외시/건동홍/시립대": [("중앙대", "0000045"), ("경희대", "0000049"), ("건국대", "0000053"),
                            ("동국대", "0000059"), ("홍익대", "0000060"), ("서울시립대", "0000115")],
    "숙명여대/세종대/가천대": [("숙명여대", "0000075"), ("세종대", "0000083"), ("가천대", "0000063")],
    "단국대/아주대/국민대 등": [("단국대", "0000089"), ("아주대", "0000090"), ("국민대", "0000078")],
    "지방 국립대": [("부산대", "0000120"), ("경북대", "0000121"), ("충남대", "0000122"),
                ("전남대", "0000123"), ("전북대", "0000124")],
    "전문대": []
}

# 목표 대학군 평균 등급 기준
target_level = {
    "의대/치대/한의대/SKY": 1.1,
    "서성한": 1.2,
    "중경외시/건동홍/시립대": 1.3,
    "숙명여대/세종대/가천대": 1.4,
    "단국대/아주대/국민대 등": 1.55,
    "지방 국립대": 2.5,
    "전문대": 3.5
}

# 평균 등급 → 대학군 분류
def predict_university(avg):
    if avg <= 1.10:
        return "의대/치대/한의대/SKY"
    elif avg <= 1.20:
        return "서성한"
    elif avg <= 1.30:
        return "중경외시/건동홍/시립대"
    elif avg <= 1.40:
        return "숙명여대/세종대/가천대"
    elif avg <= 1.55:
        return "단국대/아주대/국민대 등"
    elif avg <= 2.50:
        return "지방 국립대"
    else:
        return "전문대"

# 초기 과목 리스트
if "subjects" not in st.session_state:
    st.session_state.subjects = [
        {"name": "국어", "unit": 4, "grade": "2등급"},
        {"name": "영어", "unit": 4, "grade": "2등급"},
        {"name": "수학", "unit": 4, "grade": "2등급"},
        {"name": "사회", "unit": 3, "grade": "2등급"},
        {"name": "과학", "unit": 3, "grade": "2등급"},
        {"name": "한국사", "unit": 3, "grade": "2등급"},
    ]

# 과목 추가
st.subheader("📚 과목 추가 및 설정")
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

# 과목 리스트 표시 및 삭제
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

    result_group = predict_university(avg_grade)
    st.subheader("🎓 예상 지원 가능 대학군")
    st.success(f"👉 {result_group}")

    st.subheader("🔗 관련 대학 학과별 내신 성적 보기")
    if result_group in univ_links:
        for name, code in univ_links[result_group]:
            url = f"https://www.adiga.kr/ucp/uvt/uni/univDetailSelection.do?menuId=PCUVTINF2000&searchSyr=2026&unvCd={code}"
            st.markdown(f"- [{name} 내신 성적 보기]({url})", unsafe_allow_html=True)

    # 약한 과목
    st.subheader("💡 보완 전략: 개선하면 효과 큰 과목")
    weak_subjects = sorted(subject_grades.items(), key=lambda x: -x[1])[:2]
    for subj, score in weak_subjects:
        if score > 1.0:
            st.info(f"📌 **{subj}** 현재 {score}등급 → 성적 향상 시 전체 평균 등급 개선 효과 큼!")

    # 향상 시뮬레이션
    st.subheader("📈 시뮬레이션: 성적 향상 시 진학 가능 대학 변화")

    def simulate_avg_with_improved_grade(target_subj, new_grade):
        temp_score = 0
        for subj in st.session_state.subjects:
            name = subj["name"]
            unit = subj["unit"]
            score = grade_score[new_grade] if name == target_subj else grade_score[subj["grade"]]
            temp_score += score * unit
        return round(temp_score / total_units, 2)

    for subj_name, current_score in weak_subjects:
        st.markdown(f"#### 🎯 `{subj_name}` → 등급 향상 시 결과")
        improved_levels = [g for g, s in grade_score.items() if s < current_score]
        for improved_grade in improved_levels:
            new_avg = simulate_avg_with_improved_grade(subj_name, improved_grade)
            new_group = predict_university(new_avg)
            st.markdown(f"- `{subj_name}`을 **{improved_grade}**로 올리면 평균 등급 **{new_avg}**, 대학군 👉 **{new_group}**")

    # 시나리오별 비교
    st.subheader("🧪 시나리오별 성적 향상 분석")

    def simulate_scenario(mode="A"):
        temp_score = 0
        for subj in st.session_state.subjects:
            score = grade_score[subj["grade"]]
            if mode == "A" and subj["name"] == weak_subjects[0][0]:
                score = max(1.0, score - 1.0)
            elif mode == "B" and subj["name"] in [s[0] for s in weak_subjects]:
                score = max(1.0, score - 1.0)
            elif mode == "C":
                score = max(1.0, score - 1.0)
            temp_score += score * subj["unit"]
        return round(temp_score / total_units, 2)

    scenarios = {
        "A. 하위 1과목 1등급 향상": simulate_scenario("A"),
        "B. 하위 2과목 1등급 향상": simulate_scenario("B"),
        "C. 전 과목 1등급 향상": simulate_scenario("C")
    }

    for label, avg in scenarios.items():
        group = predict_university(avg)
        st.markdown(f"✅ `{label}` → 평균 등급 **{avg}**, 대학군 👉 **{group}**")

    # 목표 대학 비교
    st.subheader("🎯 목표 대학 입력 → 필요한 평균 등급 분석")
    goal = st.selectbox("목표 대학군 선택", list(target_level.keys()), index=1)
    required = target_level[goal]
    gap = round(avg_grade - required, 2)
    if gap <= 0:
        st.success(f"현재 성적으로 `{goal}` 진학 가능성이 높습니다! (목표 등급: {required})")
    else:
        st.warning(f"`{goal}` 진학을 위해 평균 등급 **{gap} 등급** 더 개선해야 합니다. (목표: {required})")

    # 전략 조언
    st.subheader("🧭 현실적인 전략 조언")
    def give_advice(gap):
        if gap <= 0:
            return "🎉 충분히 도전 가능한 성적입니다. 현재 과목을 유지하면서 세부 역량을 보완하세요."
        elif gap <= 0.3:
            return f"📈 `{weak_subjects[0][0]}` 과목 위주로 1등급 향상이 가능하다면 도전 가능합니다."
        elif gap <= 0.6:
            return f"💪 `{weak_subjects[0][0]}`, `{weak_subjects[1][0]}` 과목을 집중 관리해 1~2등급 개선을 노려보세요."
        else:
            return "⚠️ 현재 성적으로는 거리감이 있는 목표입니다. 논술/적성/특기자 등 다양한 전형 전략을 병행하세요."

    st.info(give_advice(gap))

st.markdown("---")
st.caption("🔍 본 분석은 2028 대입 절대평가 5등급제 및 단위수 기반 가중 평균을 기준으로 작성되었습니다.")
