import streamlit as st
import random

def card_value(card):
    if card in ["J", "Q", "K", "10"]:
        return 0
    elif card == "A":
        return 1
    else:
        return int(card)

def hand_score(hand):
    return sum(card_value(c) for c in hand) % 10

def draw_card():
    return random.choice(["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"])

def play_baccarat():
    player_hand = [draw_card(), draw_card()]
    banker_hand = [draw_card(), draw_card()]

    player_score = hand_score(player_hand)
    banker_score = hand_score(banker_hand)

    winner = "플레이어" if player_score > banker_score else "뱅커"
    if player_score == banker_score:
        winner = "타이"

    return player_hand, banker_hand, player_score, banker_score, winner

st.set_page_config(page_title="Baccarat 게임", layout="centered")
st.title("🎴 Baccarat 미니 게임")

if "balance" not in st.session_state:
    st.session_state.balance = 1000
if "history" not in st.session_state:
    st.session_state.history = []

# 💰 잔액이 없을 경우
if st.session_state.balance < 100:
    st.error("💀 잔액이 100원 미만입니다. 더 이상 베팅할 수 없습니다.\n\n앱을 새로고침하거나 초기화해 주세요.")
    st.stop()

st.markdown(f"💰 현재 잔액: **{st.session_state.balance}원**")

bet_type = st.radio("베팅할 대상 선택", ["플레이어", "뱅커", "타이"])

# ✅ 잔액 범위 내에서 베팅 금액 입력
bet_amount = st.number_input(
    "💵 베팅 금액",
    min_value=100,
    max_value=st.session_state.balance,
    step=100,
    value=100
)

if st.button("🎲 게임 시작"):
    player_hand, banker_hand, player_score, banker_score, winner = play_baccarat()

    result_text = f"""
    🧑 플레이어: {player_hand} ({player_score})  
    💼 뱅커: {banker_hand} ({banker_score})  
    👉 결과: **{winner} 승리!**
    """

    if bet_type == winner:
        if winner == "타이":
            winnings = bet_amount * 8
        elif winner == "뱅커":
            winnings = int(bet_amount * 0.95)
        else:
            winnings = bet_amount
        st.session_state.balance += winnings
        result_text += f"\n\n✅ 베팅 성공! **+{winnings}원**"
    else:
        st.session_state.balance -= bet_amount
        result_text += f"\n\n❌ 베팅 실패! **-{bet_amount}원**"

    st.markdown("---")
    st.markdown(result_text)
    st.markdown("---")

    st.session_state.history.append({
        "플레이어": player_hand,
        "뱅커": banker_hand,
        "승자": winner,
        "베팅": bet_type,
        "금액": bet_amount,
        "잔액": st.session_state.balance
    })

# 📝 기록
if st.checkbox("📋 게임 기록 보기"):
    if st.session_state.history:
        for i, r in enumerate(reversed(st.session_state.history[-10:]), 1):
            st.write(f"🎮 {i}번째 게임 - 승자: {r['승자']}, 베팅: {r['베팅']}, 금액: {r['금액']}원 → 잔액: {r['잔액']}원")
    else:
        st.info("아직 게임 기록이 없습니다.")
