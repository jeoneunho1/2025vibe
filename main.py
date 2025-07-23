import streamlit as st

# 앱 제목
st.title("🎓 2028 내신 성취도 분석기 (고교학점제 기반 + 세분화 대학 예측)")
st.caption("절대평가 5등급제 & 단위수 기반으로 내신을 계산하고, 자세한 대학 예측과 과목 추천을 해드립니다.")

# 등급 점수 매핑 (5등급제)
# 1등급: 1점, 5등급: 5점
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
    grade = st.selectbox(
        f"{subj['name']} 등급 선택", 
        list(grade_score.keys()), 
        key=subj["name"]
    )
    score = grade_score[grade]
    weighted = score * subj["unit"]
    total_score += weighted
    total_units += subj["unit"]
    subject_grades[subj["name"]] = score

# 내신 가중 평균 계산
if total_units > 0:
    avg_grade = round(total_score / total_units, 2)
    st.subheader("📊 내신 분석 결과")
    st.write(f"📌 **가중 평균 성취도 등급**: {avg_grade} 등급")
else:
    st.warning("과목을 모두 입력해주세요.")
    avg_grade = None

# 🎓 세분화된 대학 예측 함수
def predict_university(grade):
    if grade <= 1.2:
        return "🏆 서울대 / 연세대 / 고려대"
    elif grade <= 1.5:
        return "🥇 서강대 / 성균관대 / 한양대 / 이화여대"
    elif grade <= 1.8:
        return "🎯 중대 / 경희대 / 한국외대 / 서울시립대"
    elif grade <= 2.2:
        return "✅ 건국대 / 동국대 / 숙명여대 / 홍익대"
    elif grade <= 2.5:
        return "💡 가천대 / 숭실대 / 세종대 / 명지대"
    elif grade <= 2.8:
        return "📘 경기대 / 상명대 / 한성대 / 삼육대"
    elif grade <= 3.2:
        return "🔍 인하대 / 전북대 / 경북대 등 지방 국립대"
    elif grade <= 3.8:
        return "🏫 지방 사립대 / 적성전형 대학"
    else:
        return "📉 전문대 / 실기·특기자 중심 전형 추천"

# 출력 대학 예측
if avg_grade:
    st.markdown(f"🎓 **예상 가능 대학군:** {predict_university(avg_grade)}")

# 💡 과목별 보완 추천
st.subheader("💡 과목별 보완 전략 추천")
weak_subjects = sorted(subject_grades.items(), key=lambda x: -x[1])[:3]  # 성적 낮은 3과목
for subj, score in weak_subjects:
    if score >= 3.5:
        st.info(f"📌 **{subj}** 성취도 보완 필요: {score}등급 → 주요 과목이 평균을 끌어내리고 있어요.")

# 안내
st.markdown("---")
st.caption("※ 2028 대입: 절대평가 5등급제 + 단위수 가중 평균 기준입니다.")
