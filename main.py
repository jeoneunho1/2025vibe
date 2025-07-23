import streamlit as st
import random

# 카드 점수 계산 함수
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
    return player_hand, banker_hand, player_score, banker_score, winner

# 앱 설정
st.set_page_config(page_title="도박 예방 프로그램", layout="centered")

STARTING_BALANCE = 1_000_000
BET_STEP = 10_000

# 세션 초기화
if "balance" not in st.session_state:
    st.session_state.balance = STARTING_BALANCE
if "bet_amount" not in st.session_state:
    st.session_state.bet_amount = 0
if "bet_input" not in st.session_state:
    st.session_state.bet_input = 0
if "history" not in st.session_state:
    st.session_state.history = []
if "banned" not in st.session_state:
    st.session_state.banned = False
if "try_restart" not in st.session_state:
    st.session_state.try_restart = False

# ❌ 다시 시작 시 경고
if st.session_state.try_restart:
    st.markdown("""
        <div style='text-align: center; padding-top: 100px;'>
            <h1 style='font-size: 48px; color: red;'>❌ 인생에는 '다시'가 없습니다</h1>
            <h2>후회할 선택 하지 마세요.</h2>
            <p style='font-size: 20px;'>도발은 잃을 때 끝나는 것이 아니라, <strong>시작할 때부터 지고 있는 것입니다.</strong></p>
        </div>
        """, unsafe_allow_html=True)
    st.stop()

# 잠안이 없을 경우
if st.session_state.balance <= 0 or st.session_state.banned:
    st.error("💥 잔액이 0원이 되었습니다.")
    st.markdown("""
## ⚠️ 이것이 보고 보면 도발의 경우입니다.
시작할 때부터 아니해야 할 선택입니다.

#### 🚑 도움이 필요하신가요?
- 📞 도발 문제 상당전화: 1336
- 🌐 [한국도발문제관리센터 바로가기](https://www.kcgp.or.kr/portal/main/main.do)
""")
    if st.button("🔁 다시 시작하기"):
        st.session_state.try_restart = True
    st.session_state.banned = True
    st.stop()

st.title("🛑 도발 예방 프로그램")
st.markdown(f"### 💰 현재 잔액: **{st.session_state.balance:,}원**")

bet_type = st.radio("베팅할 대상", ["플레이어", "방커", "타이"])

# 금액 조절 버튼
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("➖ -10,000원"):
        new_value = max(st.session_state.bet_amount - BET_STEP, 0)
        st.session_state.bet_amount = new_value
        st.session_state.bet_input = new_value
with col2:
    if st.button("➕ +10,000원"):
        new_value = min(st.session_state.bet_amount + BET_STEP, st.session_state.balance)
        st.session_state.bet_amount = new_value
        st.session_state.bet_input = new_value
with col3:
    if st.button("💯 전액 베팅"):
        st.session_state.bet_amount = st.session_state.balance
        st.session_state.bet_input = st.session_state.balance
with col4:
    if st.button("🔀 초기화"):
        st.session_state.bet_amount = 0
        st.session_state.bet_input = 0

# 수량입력으로 베팅 금액 설정
st.session_state.bet_amount = st.number_input(
    "💵 베팅 금액 입력 (10,000원 단위)",
    min_value=0,
    max_value=st.session_state.balance,
    step=BET_STEP,
    value=st.session_state.bet_input,
    key="bet_input",
    format="%d"
)

st.markdown(f"**📌 현재 베팅 금액: {st.session_state.bet_amount:,}원**")

if st.button("🎲 게임 시작"):
    bet_amount = st.session_state.bet_amount
    if bet_amount == 0:
        st.warning("⚠️ 베팅 금액이 0원입니다.")
        st.stop()

    player_hand, banker_hand, player_score, banker_score, winner = play_baccarat()

    st.markdown("### 🎯 게임 결과")
    st.write(f"🧑 플레이어: `{player_hand}` → {player_score}점")
    st.write(f"💼 방커: `{banker_hand}` → {banker_score}점")
    st.write(f"🏆 결과: **{winner} 승리**")

    if bet_type == winner:
        if winner == "플레이어":
            payout = bet_amount
        elif winner == "방커":
            payout = int(bet_amount * 0.95)
        else:
            payout = bet_amount * 8
        st.session_state.balance += payout
        st.success(f"🎉 승리! +{payout:,}원 수익")
    else:
        st.session_state.balance -= bet_amount
        st.error(f"😞 패배! -{bet_amount:,}원 손실")

    st.markdown(f"### 💰 남은 잔액: **{st.session_state.balance:,}원**")

    if st.session_state.balance <= 0:
        st.session_state.banned = True
        st.rerun()

    st.session_state.history.append({
        "승자": winner,
        "베팅": bet_type,
        "금액": bet_amount,
        "잔액": st.session_state.balance
    })

# 최근 결과 표시
st.markdown("### 📊 최근 결과 (30개 값)")
if st.session_state.history:
    result_list = [r["승자"] for r in st.session_state.history[-30:]]
    st.write(", ".join(result_list))
else:
    st.info("최근 결과 없음")

# 게임 기록
if st.checkbox("📋 최근 게임 기록 보기"):
    if st.session_state.history:
        st.markdown("#### 📌 최근 10게임")
        for i, r in enumerate(reversed(st.session_state.history[-10:]), 1):
            st.write(f"🎮 {i} - 승자: {r['승자']}, 베팅: {r['베팅']} ({r['금액']:,}원) → 잔액: {r['잔액']:,}원")
    else:
        st.info("아직 게임 기록이 없습니다.")

# 교육 메시지
st.markdown("---")
st.markdown("""
#### 🎓 교육 메시지
> 도발은 한숟간의 쿠레러기를 위해 잠시간의 생활을 합니다.  
> 이 시뮬리언을 통해 “계속 잃고 있다”는 감각을 기억하세요.  
> **절대 시작하지 않는 것이 가장 좋은 선택입니다.**
""")
