import streamlit as st

# --- 앱 제목 ---
st.title("🎓 내신 성적 분석기 (수업시간 반영)")
st.write("과목별 등급을 입력하면 수업시수를 반영한 내신 평균과 예상 대학 수준을 알려드립니다.")

# --- 과목 및 시수 설정 ---
subject_info = {
    "국어": 4,
    "영어": 4,
    "수학": 4,
    "사회": 3,
    "과학": 3,
    "한국사": 3,
    "정보": 3
}

# --- 등급 입력 ---
st.subheader("📝 과목별 등급 입력 (1~9)")
grades = {}
for subject in subject_info:
    grades[subject] = st.selectbox(f"{subject} 등급", list(range(1, 10)), key=subject)

# --- 가중 평균 내신 계산 ---
total_score = sum(grades[subject] * subject_info[subject] for subject in grades)
total_hours = sum(subject_info.values())
weighted_avg = round(total_score / total_hours, 2)

# 주요과목 (국영수사과)
main_subjects = ["국어", "영어", "수학", "사회", "과학"]
main_score = sum(grades[s] * subject_info[s] for s in main_subjects)
main_hours = sum(subject_info[s] for s in main_subjects)
main_avg = round(main_score / main_hours, 2)

# --- 대학 예측 ---
def predict_university(avg):
    if avg <= 1.5:
        return "✅ **상위권 대학** (서성한·중경외시·서울과기대 등) 가능성이 높아요."
    elif avg <= 2.5:
        return "🎯 **인서울 대학** (건국·홍익·숭실·세종 등) 충분히 가능합니다."
    elif avg <= 3.5:
        return "🙂 **수도권 대학** (가천·경기·단국·광운 등) 지원권입니다."
    elif avg <= 4.5:
        return "🔍 **지방국립·지방 사립대** 중심으로 전략을 세워보세요."
    else:
        return "📘 **전문대·적성고사 대학** 중심으로 접근하는 것이 좋아요."

# --- 출력 결과 ---
st.subheader("📊 내신 분석 결과")
st.write(f"📌 **가중 평균 등급** (전체): {weighted_avg}")
st.write(f"📌 **주요 과목 평균** (국영수사과): {main_avg}")
st.markdown(predict_university(main_avg))

# --- 과목별 피드백 ---
st.subheader("💡 과목별 개선 팁")
if grades["영어"] >= 4:
    st.info("💡 영어 성적을 3등급 이내로 끌어올리면 상위권 가능성이 확 올라갑니다!")
if grades["수학"] >= 5:
    st.info("📐 수학 성적을 보완하면 주요과목 평균이 눈에 띄게 개선돼요.")
if grades["한국사"] >= 5:
    st.info("🗺️ 한국사 등급도 반영됩니다. 안정적인 3등급 이상 유지가 좋아요.")

# --- 리셋 안내 ---
st.markdown("---")
st.caption("※ 등급을 변경하면 자동으로 계산됩니다.")
