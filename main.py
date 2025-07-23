import streamlit as st
import random

# 🃏 카드 점수 계산
def card_value(card):
    if card in ["10", "J", "Q", "K"]:
        return 0
    elif card == "A":
        return 1
    else:
        return int(card)

# 🤖 점수 계산
def hand_score(hand):
    return sum(card_value(c) for c in hand) % 10

# 🪄 카드 한 장 뽑기
def draw_card():
    return random.choice(["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"])

# 🎲 게임 실행
def play_baccarat():
    player_hand = [draw_card(), draw_card()]
    banker_hand = [draw_card(), draw_card()]
    player_score = hand_score(player_hand)
    banker_score = hand_score(banker_hand)

    if player_score > banker_score:
        winner = "플레이어"
    elif banker_score > player_score:
        winner = "뱅커"
    else:
        winner = "타이"

    return player_hand, banker_hand, player_score, banker_score, winner

# 🌐 Streamlit 설정
st.set_page_config(page_title="Baccarat 게임", layout="centered")
st.title("🎴 실전 룰 기반 Baccarat 게임")

# 💵 설정값
STARTING_BALANCE = 100000
MIN_BET = 1000
BET_STEP = 1000

# 세션 초기화
if "balance" not in st.session_state:
    st.session_state.balance = STARTING_BALANCE
if "history" not in st.session_state:
    st.session_state.history = []
if "bet_amount" not in st.session_state:
    st.session_state.bet_amount = MIN_BET

# 💰 잔액 표시
st.markdown(f"### 💰 현재 잔액: **{st.session_state.balance:,}원**")

# 🛑 파산 처리
if st.session_state.balance < MIN_BET:
    st.error(f"💀 잔액이 {MIN_BET:,}원 미만입니다. 더 이상 베팅할 수 없습니다.")
    if st.button("🔄 잔액 초기화"):
        st.session_state.balance = STARTING_BALANCE
        st.session_state.history = []
        st.session_state.bet_amount = MIN_BET
        st.success("🎉 게임이 초기화되었습니다.")
    st.stop()

# 🎯 베팅 UI
bet_type = st.radio("어디에 베팅하시겠습니까?", ["플레이어", "뱅커", "타이"])

# 💸 베팅 금액 버튼 컨트롤
st.markdown("#### 💵 베팅 금액 조절")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("➕ +10,000원"):
        st.session_state.bet_amount = min(
            st.session_state.bet_amount + 10000, st.session_state.balance
        )
with col2:
    if st.button("💯 전액 베팅"):
        st.session_state.bet_amount = st.session_state.balance
with col3:
    if st.button("🔁 초기화"):
        st.session_state.bet_amount = MIN_BET

# 💵 베팅 금액 슬라이더
st.session_state.bet_amount = st.slider(
    "🎚️ 베팅 금액 선택",
    min_value=MIN_BET,
    max_value=st.session_state.balance,
    step=BET_STEP,
    value=st.session_state.bet_amount,
    key="bet_slider"
)

st.markdown(f"**현재 베팅 금액: {st.session_state.bet_amount:,}원**")

# ▶️ 게임 시작
if st.button("🎲 게임 시작"):
    bet_amount = st.session_state.bet_amount
    player_hand, banker_hand, player_score, banker_score, winner = play_baccarat()

    st.markdown("### 🎯 게임 결과")
    st.write(f"🧑 플레이어: `{player_hand}` → {player_score}점")
    st.write(f"💼 뱅커: `{banker_hand}` → {banker_score}점")
    st.write(f"🏆 결과: **{winner} 승!**")

    # 💵 승패 및 수익 처리
    if bet_type == winner:
        if winner == "플레이어":
            payout = bet_amount  # 1:1
        elif winner == "뱅커":
            payout = int(bet_amount * 0.95)  # 0.95:1
        elif winner == "타이":
            payout = bet_amount * 8  # 8:1
        total_gain = bet_amount + payout
        st.session_state.balance += payout
        st.success(f"✅ 베팅 성공! +{payout:,}원 수익 (총 수령: {total_gain:,}원)")
    else:
        st.session_state.balance -= bet_amount
        st.error(f"❌ 베팅 실패! -{bet_amount:,}원 손실")

    # 💰 잔액 표시
    st.markdown(f"### 💰 현재 잔액: **{st.session_state.balance:,}원**")

    # 📝 기록 저장
    st.session_state.history.append({
        "플레이어": player_hand,
        "뱅커": banker_hand,
        "승자": winner,
        "베팅": bet_type,
        "금액": bet_amount,
        "잔액": st.session_state.balance
    })

# 📋 기록 보기
if st.checkbox("📋 최근 게임 기록 보기"):
    if st.session_state.history:
        st.markdown("#### 🔁 최근 게임")
        for i, r in enumerate(reversed(st.session_state.history[-10:]), 1):
            st.write(
                f"🎮 {i} - 승자: {r['승자']}, 베팅: {r['베팅']} ({r['금액']:,}원) → 잔액: {r['잔액']:,}원"
            )
    else:
        st.info("아직 게임 기록이 없습니다.")
