import streamlit as st
import random
import pandas as pd

# 카드 점수 계산
def card_value(card):
    return 0 if card in ["10", "J", "Q", "K"] else (1 if card == "A" else int(card))

def hand_score(hand):
    return sum(card_value(c) for c in hand) % 10

def draw_card():
    return random.choice(["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"])

def play_baccarat():
    player_hand = [draw_card(), draw_card()]
    banker_hand = [draw_card(), draw_card()]
    player_score = hand_score(player_hand)
    banker_score = hand_score(banker_hand)
    winner = "플레이어" if player_score > banker_score else "뱅커" if banker_score > player_score else "타이"
    return winner

def simulate_baccarat(n_rounds=10000):
    outcomes = {"플레이어": 0, "뱅커": 0, "타이": 0}
    for _ in range(n_rounds):
        winner = play_baccarat()
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

# 세션 초기화
if "balance" not in st.session_state:
    st.session_state.balance = 1_000_000
if "bet_amount" not in st.session_state:
    st.session_state.bet_amount = 0
if "banned" not in st.session_state:
    st.session_state.banned = False
if "try_restart" not in st.session_state:
    st.session_state.try_restart = False

# 강제 종료 화면
if st.session_state.try_restart:
    st.markdown(
        """
        <div style='text-align: center; padding-top: 100px;'>
            <h1 style='font-size: 48px; color: red;'>❌ 인생에는 '다시'가 없습니다</h1>
            <h2>후회할 선택 하지 마세요.</h2>
            <p style='font-size: 20px;'>도박은 잃을 때 끝나는 게 아니라, <strong>시작할 때부터 지고 있는 겁니다.</strong></p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.stop()

# 파산 처리
if st.session_state.balance <= 0 or st.session_state.banned:
    st.error("💀 잔액이 0원이 되었습니다.")
    st.markdown("""
### ⚠️ **이게 도박의 끝입니다**
도박은 하지 않는 것이 가장 좋은 선택입니다.

---

#### 🆘 도움이 필요하신가요?
- 📞 **도박 문제 상담전화:** 1336 (24시간 운영)
- 🌐 [한국도박문제관리센터(KCGP) 바로가기](https://www.kcgp.or.kr/portal/main/main.do)
""")

    if st.button("🔄 다시 시작하기"):
        st.session_state.try_restart = True

    st.session_state.banned = True
    st.stop()

# 본 게임 화면
st.title("🎰 바카라 게임")

st.markdown(f"### 💰 현재 잔액: **{st.session_state.balance:,}원**")

with st.expander("ℹ️ 베팅 대상별 배당률 설명 보기"):
    st.markdown("""
| 🎯 베팅 대상 | 🪙 승리 시 배당률 | 설명 |
|--------------|------------------|------|
| **플레이어** | `1 : 1` | 예: 10,000원 걸면 10,000원 이익 |
| **뱅커**     | `0.95 : 1` | 예: 10,000원 걸면 9,500원 이익 (5% 수수료) |
| **타이**     | `8 : 1` | 예: 10,000원 걸면 80,000원 이익 (드물게 나옴) |
""")

bet_type = st.radio("베팅할 대상", ["플레이어", "뱅커", "타이"], horizontal=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("➖ -10,000원"):
        st.session_state.bet_amount = max(st.session_state.bet_amount - 10000, 0)
with col2:
    if st.button("➕ +10,000원"):
        st.session_state.bet_amount = min(st.session_state.bet_amount + 10000, st.session_state.balance)
with col3:
    if st.button("💯 전액 베팅"):
        st.session_state.bet_amount = st.session_state.balance
with col4:
    if st.button("🔁 초기화"):
        st.session_state.bet_amount = 0

st.slider(
    "🎚️ 베팅 금액 선택",
    min_value=0,
    max_value=st.session_state.balance,
    step=10000,
    value=st.session_state.bet_amount,
    key="bet_slider"
)

st.markdown(f"**현재 베팅 금액: {st.session_state.bet_amount:,}원**")

if st.button("🎲 게임 시작"):
    winner = play_baccarat()
    bet_amount = st.session_state.bet_amount

    if bet_type == winner:
        if winner == "플레이어":
            payout = bet_amount
        elif winner == "뱅커":
            payout = int(bet_amount * 0.95)
        else:
            payout = bet_amount * 8
        st.session_state.balance += payout
        st.success(f"✅ 베팅 성공! +{payout:,}원")
    else:
        st.session_state.balance -= bet_amount
        st.error(f"❌ 베팅 실패! -{bet_amount:,}원")

    st.markdown(f"### 💰 잔액: **{st.session_state.balance:,}원**")
    if st.session_state.balance <= 0:
        st.session_state.banned = True
        st.rerun()

# 📊 수익률/확률 분석
st.header("📊 확률 분석 및 기대 수익 시뮬레이션")

with st.spinner("📈 10,000회 시뮬레이션 중..."):
    outcomes = simulate_baccarat()
    profits = expected_profit(outcomes)

    df = pd.DataFrame({
        "승률(%)": [round(outcomes[k]/100, 2) for k in outcomes],
        "기대수익(원/1만원)": [int(profits[k]) for k in profits]
    }, index=["플레이어", "뱅커", "타이"])

    st.dataframe(df)

    st.bar_chart(df["승률(%)"])
    st.bar_chart(df["기대수익(원/1만원)"])
