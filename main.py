import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time
import random

# 기본 점심 메뉴
default_menu = ["김밥", "라면", "돈까스", "불고기", "비빔밥", "우동", "쌀국수", "햄버거"]

st.set_page_config(page_title="점심메뉴 룰렛", layout="centered")
st.title("🎯 점심메뉴 룰렛")

# 사용자 메뉴 입력
menus = st.text_input("🍱 점심 메뉴들을 쉼표(,)로 구분해서 입력해주세요:", ", ".join(default_menu))
menu_list = [m.strip() for m in menus.split(",") if m.strip()]

# 룰렛 회전 상태 저장
if "spinning" not in st.session_state:
    st.session_state.spinning = False
if "selected_index" not in st.session_state:
    st.session_state.selected_index = None
if "angle" not in st.session_state:
    st.session_state.angle = 0

def draw_wheel(angle_deg):
    num = len(menu_list)
    angles = np.linspace(0, 360, num+1)
    colors = ['#%06X' % random.randint(0, 0xFFFFFF) for _ in range(num)]

    fig = go.Figure()

    for i in range(num):
        theta = (angles[i] + angles[i+1]) / 2
        fig.add_trace(go.Pie(
            labels=[menu_list[i]],
            values=[1],
            textinfo='label',
            textposition='inside',
            marker=dict(colors=[colors[i]]),
            hole=0.3,
            direction='clockwise',
            rotation=angle_deg,
            showlegend=False
        ))

    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), width=500, height=500)
    return fig

def spin_wheel():
    st.session_state.spinning = True
    total_rotation = random.randint(360*5, 360*8)  # 5~8바퀴
    deceleration = 0.97
    speed = 20  # 초기 회전 속도 (deg/frame)
    angle = st.session_state.angle

    placeholder = st.empty()

    while speed > 0.1:
        angle += speed
        angle = angle % 360
        fig = draw_wheel(angle)
        placeholder.plotly_chart(fig, use_container_width=True)
        time.sleep(0.05)
        speed *= deceleration

    # 선택된 인덱스 계산
    slice_angle = 360 / len(menu_list)
    selected_index = int(((360 - angle) % 360) // slice_angle)
    st.session_state.selected_index = selected_index
    st.session_state.angle = angle
    st.session_state.spinning = False

# 룰렛 그리기
st.subheader("🎡 룰렛")
fig = draw_wheel(st.session_state.angle)
chart = st.plotly_chart(fig, use_container_width=True)

if st.button("🍽️ 점심 메뉴 뽑기!", disabled=st.session_state.spinning):
    spin_wheel()

if st.session_state.selected_index is not None:
    st.success(f"오늘의 점심은... **{menu_list[st.session_state.selected_index]}** 입니다! 🎉")
