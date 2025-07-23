import streamlit as st
import random

# 카드 점수 계산
def card_value(card):
    if card in ["J", "Q", "K", "10"]:
        return 0
    elif card == "A":
        return 1
    else:
        return int(card)

# 점수 합산 (10의 자리 버리기)
def hand_score(hand):
    return sum(card_value(c) for c in hand) % 10

# 카드 한 장 뽑기
def draw_card():
    return random.choice(["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"])

# 게임 실행
def play_baccarat():
    player_hand = [draw_card(), draw_card()]
    banker_hand = [draw_card(), draw_card()]

    player_score = hand_score(player_hand)
    banker_score = hand_score(banker_hand)

    # 간단화: 써드 카드 룰 무시 (더 정밀한 룰은 확장 가능)
    winner = "플레이어" if player_score > banker_score else "뱅커"
    if player_score == banker_score:
        winner = "타이"

    return player_hand, banker_hand, player_score, banker_score, winner

# 페이지 설정
st.set_page_config(page_title="Baccarat 게임", layout="centered")
st.title("🎴 Baccarat 미니 게임")

# 세션 상태 초기화
if "balance" not in st.session_state:
    st.session_state.balance = 1000  # 시작 머니
if "history" not in st.session_state:
    st.session_state.history = []

# 잔액 표시
st.markdown(f"💰 현재 잔액: **{st.session_state.balance}원**")

# 베팅 선택
bet_type = st.radio("베팅할 대상 선택", ["플레이어", "뱅커", "타이"])
bet_amount = st.number_input("💵 베팅 금액", min_value=100, max_value=st.session_state.balance, step=100)

if st.button("🎲 게임 시작"):
    player_hand, banker_hand, player_score, banker_score, winner = play_baccarat()

    result_text = f"🧑 플레이어: {player_hand} ({player_score})\n\n💼 뱅커: {banker_hand} ({banker_score})\n\n👉 결과: **{winner} 승리!**"

    # 잔액 처리
    if bet_type == winner:
        if winner == "타이":
            winnings = bet_amount * 8
        elif winner == "뱅커":
            winnings = int(bet_amount * 0.95)
        else:
            winnings = bet_amount
        st.session_state.balance += winnings
        result_text += f"\n\n✅ 베팅 성공! {winnings}원 획득"
    else:
        st.session_state.balance -= bet_amount
        result_text += f"\n\n❌ 베팅 실패! {bet_amount}원 잃음"

    st.markdown("---")
    st.markdown(result_text)
    st.markdown("---")

    # 기록 저장
    st.session_state.history.append({
        "플레이어": player_hand,
        "뱅커": banker_hand,
        "승자": winner,
        "베팅": bet_type,
        "금액": bet_amount,
        "잔액": st.session_state.balance
    })

# 게임 기록
if st.checkbox("📋 게임 기록 보기"):
    for i, r in enumerate(reversed(st.session_state.history[-10:]), 1):
        st.write(f"🎮 {i}번째 게임 - 승자: {r['승자']}, 베팅: {r['베팅']}, 금액: {r['금액']}원 → 잔액: {r['잔액']}원")
