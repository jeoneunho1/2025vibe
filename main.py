import streamlit as st

# 앱 제목
st.title("🎓 2028 내신 성취도 분석기 (최신 대학 예측 반영)")
st.caption("절대평가 5등급제 + 고정 단위수 + 세분화된 대학군 예측")

# 등급 점수 매핑
grade_score = {
    "1등급": 1.0,
    "2등급": 2.0,
    "3등급": 3.0,
    "4등급": 4.0,
    "5등급": 5.0
}

# 고정 과목과 단위수
subjects = [
    {"name": "국어", "unit": 4},
    {"name": "영어", "unit": 4},
    {"name": "수학", "unit": 4},
    {"name": "사회", "unit": 3},
    {"name": "과학", "unit": 3},
    {"name": "한국사", "unit": 3},
    {"name": "정보", "unit": 3}
]

st.subheader("📝 과목별 성취도 등급 입력 (5등급제)")
total_score = 0
total_units = 0
subject_grades = {}

for subj in subjects:
    grade = st.selectbox(f"{subj['name']} 등급", list(grade_score.keys()), key=subj["name"])
    score = grade_score[grade]
    total_score += score * subj["unit"]
    total_units += subj["unit"]
    subject_grades[subj["name"]] = score

# 평균 계산
if total_units > 0:
    avg_grade = round(total_score / total_units, 2)
    st.subheader("📊 내신 평균 등급")
    st.write(f"📌 **가중 평균 등급**: {avg_grade} 등급")
else:
    st.warning("모든 과목의 등급을 입력해주세요.")
    avg_grade = None

# 🎓 대학 예측 기준
def predict_university(avg):
    if avg <= 1.1:
        return "🏆 서울대 / 연세대 / 고려대"
    elif avg <= 1.3:
        return "🥇 서강대 / 성균관대 / 한양대 / 이화여대"
    elif avg <= 1.5:
        return "🎯 중앙대 / 경희대 / 한국외대 / 서울시립대"
    elif avg <= 1.7:
        return "✅ 건국대 / 동국대 / 홍익대"
    elif avg <= 1.9:
        return "💡 가천대 / 숭실대 / 세종대 / 명지대"
    elif avg <= 2.2:
        return "📘 경기대 / 상명대 / 한성대 / 삼육대"
    elif avg <= 2.7:
        return "🔍 지방 거점 국립대 (인하대, 전북대, 경북대 등)"
    elif avg <= 3.2:
        return "🏫 지방 사립대 / 적성고사 대학"
    else:
        return "📉 전문대 / 실기·특기자 전형 중심 접근 필요"

# 출력
if avg_grade:
    st.subheader("🎓 예상 가능 대학군")
    st.markdown(f"👉 {predict_university(avg_grade)}")

# 보완 전략
st.subheader("💡 과목별 보완 전략")
for subj, score in sorted(subject_grades.items(), key=lambda x: -x[1])[:3]:
    if score >= 3.5:
        st.info(f"📌 **{subj}** 성취도 보완이 필요합니다 (현재 {score}등급). 등급 향상이 전체 평균에 큰 영향을 줄 수 있어요!")

# 안내
st.markdown("---")
st.caption("※ 2028 대입 | 절대평가 5등급제 + 고정 단위수 기반 가중평균 분석 기준입니다.")
