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