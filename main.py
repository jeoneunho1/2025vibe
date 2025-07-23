import streamlit as st

# 앱 제목
st.title("🎓 2028 내신 성취도 분석기 (절대평가 5등급제 기반)")
st.caption("주요 과목 + 단위수 반영 평균 등급 → 세분화된 대학 예측 & 보완 전략 제공")

# 등급 점수 매핑
grade_score = {
    "1등급": 1.0,
    "2등급": 2.0,
    "3등급": 3.0,
    "4등급": 4.0,
    "5등급": 5.0
}

# 과목과 단위수
subjects = [
    {"name": "국어", "unit": 4},
    {"name": "영어", "unit": 4},
    {"name": "수학", "unit": 4},
    {"name": "사회", "unit": 3},
    {"name": "과학", "unit": 3},
    {"name": "한국사", "unit": 3},
    {"name": "정보", "unit": 3}
]

st.subheader("📝 과목별 등급 입력 (5등급제)")

subject_grades = {}
total_score = 0
total_units = 0

# 사용자 입력 받기
for subj in subjects:
    grade = st.selectbox(f"{subj['name']} 등급", list(grade_score.keys()), key=subj["name"])
    score = grade_score[grade]
    total_score += score * subj["unit"]
    total_units += subj["unit"]
    subject_grades[subj["name"]] = score

# 평균 계산
avg_grade = round(total_score / total_units, 2)

st.subheader("📊 내신 평균 등급 결과")
st.write(f"📌 **가중 평균 등급**: {avg_grade} 등급")

# 🎓 대학 예측 기준 함수
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

# 대학 예측 결과 출력
st.subheader("🎓 예상 지원 가능 대학군")
st.success(f"👉 {predict_university(avg_grade)}")

# 성적 낮은 과목 보완 전략
st.subheader("💡 보완 전략: 개선하면 효과 큰 과목")
weak_subjects = sorted(subject_grades.items(), key=lambda x: -x[1])[:2]

for subj, score in weak_subjects:
    if score > 1.0:
        st.info(f"📌 **{subj}** 현재 {score}등급 → 성적 향상 시 전체 평균 등급 개선 효과 큼!")

# 안내
st.markdown("---")
st.caption("🔍 본 분석은 2028 대입 절대평가 5등급제 + 단위수 기반 내신 가중 평균을 기준으로 합니다.")
