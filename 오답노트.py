import streamlit as st

st.title("📘 오답노트 / 학습 피드백")

wrong_q = st.text_area("문제 요약", key="wrong_q")
reflection = st.text_area("틀린 이유 / 기억할 점", key="wrong_ref")

if st.button("📌 오답 저장"):
    st.session_state.setdefault("wrong_notes", []).append((wrong_q, reflection))
    st.success("오답노트에 저장되었습니다.")

if "wrong_notes" in st.session_state:
    st.markdown("### 🔍 저장된 오답노트")
    for i, (q, r) in enumerate(st.session_state["wrong_notes"], 1):
        st.markdown(f"**{i}. 문제 요약:** {q}")
        st.markdown(f"👉 피드백: {r}")
        st.markdown("---")