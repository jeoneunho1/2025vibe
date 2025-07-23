import streamlit as st

# 앱 제목
st.title("🎓 2028 내신 성취도 분석기")
st.write("고정된 이수 단위와 5등급제 성취도를 기준으로 내신 평균과 대학 가능성을 분석합니다.")

# 5등급제 성취도 → 점수 매핑
grade_point = {
    "A": 1.0,
    "B": 2.0,
    "C": 3.0,
    "D": 4.0,
    "E": 5.0
}

# 고정 과목 리스트와 단위 수
subjects = [
    {"name": "국어", "unit": 4},
    {"name": "영어", "unit": 4},
    {"name": "수학", "unit": 4},
    {"name": "사회", "unit": 3},
    {"name": "과학", "unit": 3},
    {"name": "한국사", "unit": 3},
    {"name": "정보", "unit": 3}
]

# 성취도 입력
st.subheader("📝 과목별 성취도 입력 (5등급제)")
total_score = 0
total_units = 0

for subject in subjects:
    grade = st.selectbox(f"{subject['name']} 성취도", ["A", "B", "C", "D", "E"], key=subject["name"])
    point = grade_point[grade]
    total_score += point * subject["unit"]
    total_units += subject["unit"]

# 평균 계산
if total_units > 0:
    avg_score = round(total_score / total_units, 2)
else:
    avg_score = None

# 대학 예측 함수
def predict_college(avg):
    if avg <= 1.2:
        return "🏆 **SKY (서울대/연세대/고려대)** 진학 가능 수준입니다."
    elif avg <= 1.5:
        return "🥇 **서성한·중경외시·서울시립대** 진학권입니다."
    elif avg <= 2.0:
        return "🎯 **건국대, 홍익대, 숙명여대 등 인서울 중위권 대학** 가능성이 높아요."
    elif avg <= 2.5:
        return "✅ **수도권 상위 or 지방거점국립대** 진학 전략이 좋습니다."
    elif avg <= 3.0:
        return "🙂 **수도권 하위권 or 지방 국립대** 지원권입니다."
    elif avg <= 4.0:
        return "📘 **지방 사립대, 적성고사 대학** 추천됩니다."
    else:
        return "🔍 **전문대, 실기/특기자 전형 중심** 전략이 필요합니다."

# 결과 출력
st.subheader("📊 분석 결과")
if avg_score:
    st.write(f"📌 **가중 평균 성취도 등급**: {avg_score}")
    st.markdown(predict_college(avg_score))
else:
    st.warning("과목 성취도를 모두 입력해주세요.")

# 안내
st.markdown("---")
st.caption("※ 2028 대입 기준: 절대평가 5등급제 + 고정 단위 기반 분석입니다.")
