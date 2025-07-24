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
if "bet_input" not in st.session_state:
    st.session_state.bet_input = 0
if "history" not in st.session_state:
    st.session_state.history = []
if "banned" not in st.session_state:
    st.session_state.banned = False
if "try_restart" not in st.session_state:
    st.session_state.try_restart = False
if "purchases" not in st.session_state:
    st.session_state.purchases = []

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

st.markdown("#### 🎚️ 베팅 금액 조절")
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
    if st.button("🔁 초기화"):
        st.session_state.bet_amount = 0
        st.session_state.bet_input = 0

# 베팅 금액 직접 입력
st.session_state.bet_amount = st.number_input(
    "💵 베팅 금액 입력 (10,000원 단위)",
    min_value=0,
    max_value=st.session_state.balance,
    step=BET_STEP,
    value=st.session_state.bet_input,
    key="bet_input",
    format="%d"
)

# 슬라이더도 다시 추가
st.slider(
    "🔧 베팅 금액 슬라이더",
    min_value=0,
    max_value=st.session_state.balance,
    step=BET_STEP,
    value=st.session_state.bet_amount,
    key="bet_slider"
)

st.markdown(f"**📌 현재 베팅 금액: {st.session_state.bet_amount:,}원**")

# 게임 실행
if st.button("🎲 게임 시작"):
    bet_amount = st.session_state.bet_amount

    if bet_amount == 0:
        st.warning("⚠️ 베팅 금액이 0원입니다.")
        st.stop()

    player_hand, banker_hand, player_score, banker_score, winner = play_baccarat()

    st.markdown("### 🎯 게임 결과")
    st.write(f"🧑 플레이어: `{player_hand}` → {player_score}점")
    st.write(f"💼 뱅커: `{banker_hand}` → {banker_score}점")
    st.write(f"🏆 결과: **{winner} 승리**")

    if bet_type == winner:
        if winner == "플레이어":
            payout = bet_amount
        elif winner == "뱅커":
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
        "플레이어": player_hand,
        "뱅커": banker_hand,
        "승자": winner,
        "베팅": bet_type,
        "금액": bet_amount,
        "잔액": st.session_state.balance
    })

# 결과 시각화
if st.session_state.history:
    st.markdown("### 🧾 최근 결과 기록")
    results = " → ".join([r['승자'] for r in st.session_state.history[-30:]])
    st.code(results)

# 📋 기록
if st.checkbox("📋 최근 게임 기록 보기"):
    if st.session_state.history:
        st.markdown("#### 📌 최근 10게임 기록")
        for i, r in enumerate(reversed(st.session_state.history[-10:]), 1):
            st.write(f"🎮 {i} - 승자: {r['승자']}, 베팅: {r['베팅']} ({r['금액']:,}원) → 잔액: {r['잔액']:,}원")
    else:
        st.info("아직 게임 기록이 없습니다.")

# 🛍 아이템 구매
st.markdown("---")
st.header("🎁 수익으로 가치 있는 소비하기")
items = {
    "📚 책 1권 (15,000원)": (15000, "지식은 잃지 않습니다."),
    "🖥 중고 노트북 (300,000원)": (300000, "기회는 준비된 사람에게 옵니다."),
    "🎧 무선 이어폰 (120,000원)": (120000, "잠깐의 유흥보다 오래 쓰는 가치"),
    "🎓 학원 수강권 (500,000원)": (500000, "이 돈, 투자였으면 얼마나 좋았을까?"),
}
item_choice = st.selectbox("구매할 수 있는 물건을 선택하세요", list(items.keys()))

if st.button("🛍 구매하기"):
    price, msg = items[item_choice]
    if st.session_state.balance >= price:
        st.session_state.balance -= price
        st.session_state.purchases.append(item_choice)
        st.success(f"'{item_choice}' 구매 완료! ✨\n👉 {msg}")
    else:
        st.warning("잔액이 부족합니다. 도박으로는 원하는 걸 살 수 없습니다.")

if st.session_state.purchases:
    st.markdown("#### 🧾 구매한 물건들")
    for item in st.session_state.purchases:
        st.write(f"✅ {item}")

# 교육 메시지
st.markdown("---")
st.markdown("""
#### 🎓 교육 메시지
> 도박은 한순간의 쾌락을 위해 장기적인 삶을 희생할 수 있습니다.  
> 이 시뮬레이션을 통해 "계속 잃고 있다는 감각"을 기억하세요.  
> **절대 시작하지 않는 것이 가장 좋은 선택입니다.**
""")
