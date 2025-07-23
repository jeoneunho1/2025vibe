import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Plinko 시뮬레이터", layout="wide")
st.title("🪙 Plinko 시뮬레이터")
st.caption("핀을 통과하며 공이 떨어지는 경로를 시뮬레이션합니다.")

# 사용자 입력
num_balls = st.slider("🎯 공의 개수", min_value=1, max_value=500, value=100)
depth = st.slider("📐 보드 깊이 (핀 행 수)", min_value=3, max_value=15, value=10)

if st.button("🎲 시뮬레이션 시작"):
    # 시뮬레이션
    final_positions = []

    for _ in range(num_balls):
        position = 0
        for _ in range(depth):
            step = np.random.choice([0, 1])  # 왼쪽 또는 오른쪽
            position += step
        final_positions.append(position)

    # 결과 집계
    bins = depth + 1
    results = np.zeros(bins, dtype=int)
    for pos in final_positions:
        results[pos] += 1

    # 시각화
    st.subheader("📊 결과: 슬롯 별 공 개수")
    fig, ax = plt.subplots()
    ax.bar(range(bins), results, tick_label=[str(i) for i in range(bins)])
    ax.set_xlabel("슬롯 번호")
    ax.set_ylabel("공 개수")
    ax.set_title("Plinko 슬롯 도착 분포")
    st.pyplot(fig)

    # 텍스트 출력 (선택적)
    st.subheader("📝 슬롯 별 결과 요약")
    for i, count in enumerate(results):
        st.write(f"슬롯 {i}: {count}개")
