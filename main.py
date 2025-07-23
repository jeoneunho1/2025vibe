import streamlit as st
import datetime
import json
import os
import plotly.graph_objects as go

# --- 파일 저장 경로 ---
DATA_FILE = "tracker_data.json"

# --- 초기 데이터 불러오기 또는 생성 ---
if "data" not in st.session_state:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            st.session_state.data = json.load(f)
    else:
        st.session_state.data = {}

# --- 오늘 날짜 키 ---
today = datetime.date.today().isoformat()
if today not in st.session_state.data:
    st.session_state.data[today] = {
        "mood": None,
        "todos": [],
        "times": {},
        "note": ""
    }

day_data = st.session_state.data[today]

# --- 앱 UI 시작 ---
st.title("🧠 MyLife Tracker")
st.subheader(f"📅 {today} | 오늘 하루 어땠나요?")

# --- 감정 선택 ---
moods = {"😊": "좋음", "😐": "보통", "😢": "슬픔", "😠": "화남", "😍": "사랑"}
selected_mood = st.radio(
    "기분 선택", 
    list(moods.keys()), 
    index=list(moods.keys()).index(day_data["mood"]) if day_data["mood"] else 1, 
    horizontal=True
)
day_data["mood"] = selected_mood

# --- 할 일 입력 및 관리 ---
st.markdown("## ✅ 오늘의 할 일")
todo_input = st.text_input("할 일 추가")
if st.button("➕ 추가") and todo_input:
    day_data["todos"].append({"task": todo_input, "done": False})

for i, t in enumerate(day_data["todos"]):
    col1, col2 = st.columns([0.1, 0.9])
    checked = col1.checkbox("", value=t["done"], key=f"todo_{i}")
    col2.write(f"~~{t['task']}~~" if checked else t["task"])
    day_data["todos"][i]["done"] = checked

# --- 시간 사용 기록 ---
st.markdown("## ⏱️ 오늘 시간 사용 기록")
activities = ["업무", "공부", "운동", "휴식", "기타"]
for act in activities:
    time = st.number_input(
        f"{act}에 사용한 시간 (시간 단위)", 
        min_value=0.0, max_value=24.0, step=0.5, 
        value=day_data["times"].get(act, 0.0)
    )
    day_data["times"][act] = time

# --- 메모 섹션 ---
st.markdown("## 📝 하루 한 줄 회고")
day_data["note"] = st.text_area("오늘을 돌아보며", value=day_data["note"])

# --- 감정 및 시간 요약 시각화 ---
st.markdown("## 📊 감정 & 시간 요약")

# 1. 감정 추이 (최근 7일)
mood_history = [
    st.session_state.data[d]["mood"] 
    for d in sorted(st.session_state.data.keys())[-7:] 
    if st.session_state.data[d]["mood"]
]
if mood_history:
    mood_score = [list(moods.keys()).index(m) for m in mood_history]
    st.line_chart(mood_score)

# 2. 시간 도넛 차트
labels = list(day_data["times"].keys())
values = list(day_data["times"].values())

if sum(values) > 0:
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        textinfo='label+percent'
    )])
    fig.update_layout(title_text="오늘 시간 사용 비율")
    st.plotly_chart(fig)

# --- 데이터 저장 ---
with open(DATA_FILE, "w") as f:
    json.dump(st.session_state.data, f)

# --- 주간 요약 (일요일만 표시) ---
if datetime.date.today().weekday() == 6:
    st.markdown("## 📈 이번 주 요약")
    week_days = [datetime.date.today() - datetime.timedelta(days=i) for i in range(6, -1, -1)]
    for day in week_days:
        d_str = day.isoformat()
        if d_str in st.session_state.data:
            entry = st.session_state.data[d_str]
            mood = entry["mood"] or "❓"
            done_count = sum(1 for t in entry["todos"] if t["done"])
            total = len(entry["todos"])
            st.write(f"{d_str} | 기분: {mood} | 할 일 완료: {done_count}/{total}")
