import streamlit as st
import matplotlib.pyplot as plt
# 📊 수익률 및 확률 분석
st.header("📊 확률 분석 및 기대 수익 시뮬레이션")

def simulate_baccarat(n_rounds=10000):
    outcomes = {"플레이어": 0, "뱅커": 0, "타이": 0}
    for _ in range(n_rounds):
        player_hand = [draw_card(), draw_card()]
        banker_hand = [draw_card(), draw_card()]
        player_score = hand_score(player_hand)
        banker_score = hand_score(banker_hand)
        winner = "플레이어" if player_score > banker_score else "뱅커" if banker_score > player_score else "타이"
        outcomes[winner] += 1
    return outcomes

def expected_profit(outcomes, total_rounds=10000):
    profit = {}
    for bet in outcomes:
        win_rate = outcomes[bet] / total_rounds
        if bet == "플레이어":
            profit[bet] = win_rate * 10000 - (1 - win_rate) * 10000
        elif bet == "뱅커":
            profit[bet] = win_rate * 9500 - (1 - win_rate) * 10000
        elif bet == "타이":
            profit[bet] = win_rate * 80000 - (1 - win_rate) * 10000
    return profit

with st.spinner("📈 10,000회 시뮬레이션 중..."):
    outcomes = simulate_baccarat()
    profits = expected_profit(outcomes)

    st.subheader("🎲 승률 분석")
    for k, v in outcomes.items():
        st.write(f"✅ {k} 승률: {v / 10000:.2%}")

    st.subheader("💸 기대 수익 (1만원당)")
    for k, v in profits.items():
        st.write(f"💰 {k}에 1만원 베팅 시 기대 수익: **{int(v):,}원**")

    # 그래프
    import matplotlib.pyplot as plt

    labels = list(outcomes.keys())
    values = [outcomes[k] / 100 for k in labels]
    fig1, ax1 = plt.subplots()
    ax1.bar(labels, values, color=["skyblue", "lightgreen", "lightcoral"])
    ax1.set_title("🏆 베팅 대상별 승률 (%)")
    ax1.set_ylabel("승률 (%)")

    fig2, ax2 = plt.subplots()
    values2 = [profits[k] for k in labels]
    ax2.bar(labels, values2, color=["skyblue", "lightgreen", "lightcoral"])
    ax2.set_title("💸 베팅 대상별 기대 수익 (원)")
    ax2.set_ylabel("기대 수익 (1만원 기준)")

    st.pyplot(fig1)
    st.pyplot(fig2)
