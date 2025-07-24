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

# 초기 값
STARTING_BALANCE = 1_000_000
BET_STEP = 10_000

# 세션 상태 초기화
if "balance" not in st.session_state:
    st.session_state.balance = STARTING_BALANCE
if "bet_amount" not in st.session_state:
    st.session_state.bet_amount = 0
if "history" not in st.session_state:
    st.session_state.history = []
if "banned" not in st.session_state:
    st.session_state.banned = False
if "try_restart" not in st.session_state:
    st.session_state.try_restart = False
if "upgrades" not in st.session_state:
    st.session_state.upgrades = {}
if "effects" not in st.session_state:
    st.session_state.effects = {
        "타이 확정": False,
        "2배 수익": False,
        "승률 증가": None
    }

# ❌ 다시 시작 클릭 시 경고 화면
if st.session_state.try_restart:
    st.markdown("""
        <div style='text-align: center; padding-top: 100px;'>
            <h1 style='font-size: 48px; color: red;'>❌ 인생에는 '다시'가 없습니다</h1>
            <h2>후회할 선택 하지 마세요.</h2>
            <p style='font-size: 20px;'>도박은 잃을 때 끝나는 게 아니라, <strong>시작할 때부터 지고 있는 겁니다.</strong></p>
        </div>
        """, unsafe_allow_html=True)
    st.stop()

# 타이틀
st.title("🛑 도박 예방 프로그램")
st.caption("이 시뮬레이션은 도박의 위험성을 체감하고, 그 결과가 얼마나 불확실한지를 보여주기 위한 교육용 도구입니다.")

# 💀 파산 시 경고 출력
if st.session_state.balance <= 0 or st.session_state.banned:
    st.error("💥 잔액이 0원이 되었습니다.")
    st.markdown("""
## ⚠️ 이게 바로 도박의 끝입니다.
도박은 시작하는 순간부터 이미 손해일 수 있습니다.  
더 이상 손실이 커지기 전에 지금 멈추세요.

#### 🆘 도움이 필요하신가요?
- 📞 도박 문제 상담전화: 1336 (24시간 운영)
- 🌐 [한국도박문제관리센터 바로가기](https://www.kcgp.or.kr/portal/main/main.do)
""")
    if st.button("🔁 다시 시작하기"):
        st.session_state.try_restart = True
    st.session_state.banned = True
    st.stop()

# 잔액 및 베팅
st.markdown(f"### 💰 현재 잔액: **{st.session_state.balance:,}원**")

bet_type = st.radio("베팅할 대상", ["플레이어", "뱅커", "타이"])

# 베팅 금액 입력
bet_input = st.number_input("💵 베팅 금액 입력 (10,000원 단위)",
                            min_value=0,
                            max_value=st.session_state.balance,
                            step=BET_STEP,
                            format="%d")
st.session_state.bet_amount = bet_input

# 슬라이더
slider_value = st.slider("🎚️ 베팅 금액 슬라이더", 0, st.session_state.balance, bet_input, BET_STEP)
if slider_value != bet_input:
    st.session_state.bet_amount = slider_value
    bet_input = slider_value

# 버튼들
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("➖ -10,000원"):
        st.session_state.bet_amount = max(st.session_state.bet_amount - BET_STEP, 0)
with col2:
    if st.button("➕ +10,000원"):
        st.session_state.bet_amount = min(st.session_state.bet_amount + BET_STEP, st.session_state.balance)
with col3:
    if st.button("💯 전액 베팅"):
        st.session_state.bet_amount = st.session_state.balance
with col4:
    if st.button("🔁 초기화"):
        st.session_state.bet_amount = 0

st.markdown(f"**📌 현재 베팅 금액: {st.session_state.bet_amount:,}원**")

# 게임 실행
if st.button("🎲 게임 시작"):
    bet_amount = st.session_state.bet_amount

    if bet_amount == 0:
        st.warning("⚠️ 베팅 금액이 0원입니다.")
        st.stop()

    if st.session_state.effects["타이 확정"]:
        winner = "타이"
        st.session_state.effects["타이 확정"] = False
        player_hand = ["?", "?"]
        banker_hand = ["?", "?"]
        player_score = 0
        banker_score = 0
    else:
        player_hand, banker_hand, player_score, banker_score, winner = play_baccarat()

    st.markdown("### 🎯 게임 결과")
    st.write(f"🧑 플레이어: `{player_hand}` → {player_score}점")
    st.write(f"💼 뱅커: `{banker_hand}` → {banker_score}점")
    st.write(f"🏆 결과: **{winner} 승리**")

    payout = 0
    if bet_type == winner:
        if winner == "플레이어":
            payout = bet_amount
        elif winner == "뱅커":
            payout = int(bet_amount * 0.95)
        else:
            payout = bet_amount * 8

        if st.session_state.effects["2배 수익"]:
            payout *= 2
            st.session_state.effects["2배 수익"] = False

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
        "플레이어": player_hand,
        "뱅커": banker_hand,
        "승자": winner,
        "베팅": bet_type,
        "금액": bet_amount,
        "잔액": st.session_state.balance
    })

# 아이템 상점
st.markdown("---")
st.header("🧨 아이템 상점")
item_shop = {
    "타이 확정": (800_000, "다음 게임에서 무조건 타이 결과가 나옵니다."),
    "2배 수익": (500_000, "다음 승리 시 수익이 2배로 들어옵니다."),
    "플레이어 확률 증가": (400_000, "플레이어가 이길 확률이 소폭 증가합니다 (시뮬레이션용)."),
    "뱅커 확률 증가": (400_000, "뱅커가 이길 확률이 소폭 증가합니다 (시뮬레이션용).")
}
for name, (price, desc) in item_shop.items():
    if st.button(f"💠 {name} 구매 ({price:,}원)"):
        if st.session_state.balance >= price:
            st.session_state.balance -= price
            if name == "타이 확정":
                st.session_state.effects["타이 확정"] = True
            elif name == "2배 수익":
                st.session_state.effects["2배 수익"] = True
            elif name == "플레이어 확률 증가":
                st.session_state.effects["승률 증가"] = "플레이어"
            elif name == "뱅커 확률 증가":
                st.session_state.effects["승률 증가"] = "뱅커"
            st.success(f"'{name}' 아이템 구매 완료!")
        else:
            st.warning("잔액이 부족합니다.")
        st.caption(desc)

# 교육 메시지
st.markdown("---")
st.markdown("""
#### 🎓 교육 메시지
> 도박은 한순간의 쾌락을 위해 장기적인 삶을 희생할 수 있습니다.  
> 이 시뮬레이션을 통해 "계속 잃고 있다는 감각"을 기억하세요.  
> **절대 시작하지 않는 것이 가장 좋은 선택입니다.**
""")
