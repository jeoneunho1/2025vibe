import streamlit as st

st.set_page_config(page_title="2028 대입 분석기", layout="wide")

st.title("🎓 2028 대입 전략 통합 분석기")
st.markdown("""
이 앱은 다음 기능을 제공합니다:

- **내신 분석**: 가중평균 등급 → 대학 예측
- **모의고사 분석**: 수시 vs 정시 전략 추천
- **성적 시뮬레이션**: 특정 과목 향상 시 예측 변화
- **일정 관리**: 입시 일정 정리 및 확인
- **오답노트**: 틀린 문제 정리 및 복습 관리

👉 왼쪽 사이드바에서 각 기능별 페이지로 이동하세요.
""")

import streamlit as st

grade_score = {"1등급": 1.0, "2등급": 2.0, "3등급": 3.0, "4등급": 4.0, "5등급": 5.0}
target_level = {
    "의대/치대/한의대/SKY": 1.1, "서성한": 1.2, "중경외시/건동홍/시립대": 1.3,
    "숙명여대/세종대/가천대": 1.4, "단국대/아주대/국민대 등": 1.55,
    "지방 국립대": 2.5, "전문대": 3.5
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
    name = st.text_input("과목명 (예: 정보)")
    unit = st.number_input("단위수", 1, 10, value=3)
    grade = st.selectbox("등급", list(grade_score.keys()))
    if st.form_submit_button("과목 추가") and name:
        st.session_state.subjects.append({"name": name, "unit": unit, "grade": grade})
        st.success(f"{name} 과목이 추가되었습니다.")

for i, subj in enumerate(st.session_state.subjects):
    c1, c2, c3 = st.columns([3, 2, 2])
    subj["name"] = c1.text_input(f"과목명 {i+1}", subj["name"], key=f"name_{i}")
    subj["unit"] = c2.number_input(f"단위수 {i+1}", 1, 10, subj["unit"], key=f"unit_{i}")
    subj["grade"] = c3.selectbox(f"등급 {i+1}", list(grade_score.keys()), index=list(grade_score).index(subj["grade"]), key=f"grade_{i}")

# 분석 결과 출력
total_score = sum(grade_score[s["grade"]] * s["unit"] for s in st.session_state.subjects)
total_units = sum(s["unit"] for s in st.session_state.subjects)
avg_grade = round(total_score / total_units, 2)
group = predict_university(avg_grade)
st.success(f"📌 내신 평균 등급: **{avg_grade}**, 예측 대학군: **{group}**")

import streamlit as st

st.title("📝 모의고사 분석 & 정시/수시 전략")

st.markdown("#### 모의고사 과목별 백분위 입력")
mock_scores = {}
for subj in ["국어", "수학", "영어", "탐구1", "탐구2"]:
    mock_scores[subj] = st.number_input(f"{subj} 백분위", 0, 100, step=1, key=f"mock_{subj}")

mock_avg = round(sum(mock_scores.values()) / len(mock_scores), 2)
st.info(f"📊 평균 백분위: **{mock_avg}**")

st.subheader("🎯 전략 추천")
if mock_avg >= 96:
    st.success("✅ 정시 중심 전략 추천 (상위권 가능)")
elif mock_avg <= 85:
    st.info("📌 수시 위주 전략 추천")
else:
    st.warning("📌 수시 + 정시 병행 전략 추천")

import streamlit as st

grade_score = {"1등급": 1.0, "2등급": 2.0, "3등급": 3.0, "4등급": 4.0, "5등급": 5.0}
target_level = {
    "의대/치대/한의대/SKY": 1.1, "서성한": 1.2, "중경외시/건동홍/시립대": 1.3,
    "숙명여대/세종대/가천대": 1.4, "단국대/아주대/국민대 등": 1.55,
    "지방 국립대": 2.5, "전문대": 3.5
}

def predict_university(avg):
    for group, threshold in target_level.items():
        if avg <= threshold:
            return group
    return "전문대"

st.title("📈 성적 향상 시뮬레이션")

if "subjects" not in st.session_state or len(st.session_state.subjects) == 0:
    st.warning("📌 먼저 내신 과목을 입력해주세요.")
else:
    subj_list = [s["name"] for s in st.session_state.subjects]
    target_subj = st.selectbox("향상할 과목", subj_list)
    target_grade = st.selectbox("목표 등급", list(grade_score.keys()))

    total_units = sum(s["unit"] for s in st.session_state.subjects)
    sim_score = 0
    for subj in st.session_state.subjects:
        score = grade_score[target_grade] if subj["name"] == target_subj else grade_score[subj["grade"]]
        sim_score += score * subj["unit"]
    sim_avg = round(sim_score / total_units, 2)
    sim_group = predict_university(sim_avg)

    st.success(f"✅ `{target_subj}`을 **{target_grade}**로 올리면 평균: **{sim_avg}**, 예측 대학군: **{sim_group}**")

import streamlit as st
from datetime import date

st.title("📅 입시 일정 관리")

event = st.text_input("일정 내용 입력")
event_date = st.date_input("일정 날짜", date.today())

if st.button("➕ 일정 추가"):
    st.session_state.setdefault("schedules", []).append((event_date, event))
    st.success("✅ 일정이 추가되었습니다.")

if "schedules" in st.session_state:
    st.markdown("### 🗓️ 등록된 일정")
    for d, e in sorted(st.session_state["schedules"]):
        st.markdown(f"- {d.strftime('%Y-%m-%d')} : **{e}**")

import streamlit as st

st.title("📘 오답노트 / 학습 피드백")

q = st.text_area("문제 요약 또는 개념", key="wrong_q")
r = st.text_area("오답 이유 및 기억할 점", key="wrong_ref")

if st.button("📌 오답 저장"):
    st.session_state.setdefault("wrong_notes", []).append((q, r))
    st.success("오답노트에 저장되었습니다.")

if "wrong_notes" in st.session_state:
    st.markdown("### 🔍 저장된 오답노트")
    for i, (q, r) in enumerate(st.session_state["wrong_notes"], 1):
        st.markdown(f"**{i}. 문제 요약:** {q}")
        st.markdown(f"👉 복습 메모:** {r}")
        st.markdown("---")
