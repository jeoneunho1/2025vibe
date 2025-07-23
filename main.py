import streamlit as st

# --- 앱 제목 ---
st.title("🎓 내신 성적 분석기 (5등급제)")
st.write("과목별 5등급제를 기준으로 내신 평균과 대학 진학 가능성을 분석해드립니다!")

# --- 과목 및 수업시수 정보 ---
subject_info = {
    "국어": 4,
    "영어": 4,
    "수학": 4,
    "사회": 3,
    "과학": 3,
    "한국사": 3,
    "정보": 3
}

# --- 등급 입력 (1.0~5.0, 0.5 간격) ---
st.subheader("📝 과목별 성적 입력 (5등급제)")
grade_options = [round(x * 0.5, 1) for x in range(2, 11)]  # 1.0 ~ 5.0
grades = {}
for subject in subject_info:
    grades[subject] = st.selectbox(f"{subject} 등급", grade_options, key=subject)

# --- 가중 평균 계산 ---
total_score = sum(grades[s] * subject_info[s] for s in grades)
total_hours = sum(subject_info.values())
weighted_avg = round(total_score / total_hours, 2)

main_subjects = ["국어", "영어", "수학", "사회", "과학"]
main_score = sum(grades[s] * subject_info[s] for s in main_subjects)
main_hours = sum(subject_info[s] for s in main_subjects)
main_avg = round(main_score / main_hours, 2)

# --- 대학 예측 함수 (5등급 기준) ---
def predict_university(avg):
    if avg <= 1.2:
        return "🏆 **SKY (서울대, 연세대, 고려대)** 진학 가능성을 기대할 수 있어요."
    elif avg <= 1.6:
        return "🥇 **서성한·중경외시·서울시립대** 진학권입니다."
    elif avg <= 2.0:
        return "🎯 **건국대, 홍익대, 숙명여대, 숭실대 등 인서울 중위권** 가능성이 높아요."
    elif avg <= 2.5:
        return "✅ **가천대, 광운대, 명지대, 상명대 등 수도권 상위 대학** 지원 가능권입니다."
    elif avg <= 3.0:
        return "🙂 **경기대, 한성대, 덕성여대 등 수도권 하위 대학**도 충분히 노려볼 수 있어요."
    elif avg <= 3.5:
        return "🔍 **지방 국립대, 지역거점대** 중심 전략이 좋아요."
    elif avg <= 4.0:
        return "🏫 **지방 사립대, 적성고사 전형** 위주로 접근해보세요."
    else:
        return "📘 **전문대/실기전형/특기자 전형** 전략이 필요합니다."

# --- 결과 출력 ---
st.subheader("📊 분석 결과")
st.write(f"📌 **전체 가중 평균 등급**: {weighted_avg}")
st.write(f"📌 **주요과목 평균 등급 (국영수사과)**: {main_avg}")
st.markdown(predict_university(main_avg))

# --- 피드백 ---
st.subheader("💡 과목별 개선 팁")
if grades["영어"] >= 3.5:
    st.info("💡 영어는 수능과 비교과 모두 중요합니다. 3등급 이내 유지가 좋아요.")
if grades["수학"] >= 4.0:
    st.info("📐 수학 성적을 올리면 자연계/공대 진학 시 더 유리합니다.")
if grades["한국사"] >= 4.0:
    st.info("🗺️ 한국사는 수시 가산점에 영향이 있으니 3등급 이상 유지 추천!")

# --- 안내 ---
st.markdown("---")
st.caption("※ 모든 계산은 수업 시수 기반 가중 평균으로 처리됩니다.")
