import streamlit as st

# --- 앱 제목 ---
st.title("🎓 내신 성적 분석기")
st.write("과목별 등급을 입력하면 내신 평균과 예상 대학 수준을 분석해드립니다!")

# --- 과목 리스트 ---
subjects = ["국어", "수학", "영어", "사회", "과학", "한국사", "기술가정", "도덕", "음악", "미술", "체육"]

st.subheader("📝 과목별 등급 입력")
grades = {}
for subject in subjects:
    grades[subject] = st.selectbox(f"{subject} 등급", [1, 2, 3, 4, 5, 6, 7, 8, 9], key=subject)

# --- 평균 내신 계산 ---
total_avg = round(sum(grades.values()) / len(grades), 2)

# 주요과목 기준 (국영수사과)
main_subjects = ["국어", "수학", "영어", "사회", "과학"]
main_avg = round(sum(grades[s] for s in main_subjects) / len(main_subjects), 2)

# --- 결과 분석 ---
def estimate_university(avg):
    if avg <= 1.5:
        return "✅ **상위권 대학** (서성한/중경외시/서울과기대 등) 가능성이 높아요."
    elif avg <= 2.5:
        return "🎯 **인서울 대학** (건국/홍익/숭실/세종 등) 충분히 가능합니다."
    elif avg <= 3.5:
        return "🙂 **수도권 대학** (가천/경기/단국/광운 등) 지원권입니다."
    elif avg <= 4.5:
        return "🔍 **지방국립/지방 사립대** 중심 지원을 고려해보세요."
    else:
        return "📘 **전문대/특성화대/적성고사 대학** 중심으로 전략을 짜야 해요."

# --- 출력 결과 ---
st.subheader("📊 내신 결과 분석")
st.write(f"📌 **전체 평균 등급**: {total_avg}")
st.write(f"📌 **주요 과목 평균 (국영수사과)**: {main_avg}")

st.markdown(estimate_university(main_avg))

# --- 추가 피드백 ---
if total_avg <= 2.0 and grades["영어"] >= 4:
    st.info("💡 영어 등급을 조금 더 끌어올리면 상위권 대학 가능성이 훨씬 높아져요!")
elif grades["수학"] >= 5:
    st.info("📐 수학 성적 향상이 전체 내신 상승에 크게 도움이 될 수 있어요!")

# --- 리셋 안내 ---
st.markdown("---")
st.caption("Tip: 등급을 바꾸면 실시간으로 분석 결과가 자동 갱신돼요.")
