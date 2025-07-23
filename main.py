import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time
import random

st.set_page_config(page_title="점심메뉴 룰렛", layout="centered")
st.title("🎯 점심메뉴 룰렛")

default_menu = ["김밥", "라면", "돈까스", "불고기", "비빔밥", "우동", "쌀국수", "햄버거"]
menus = st.text_input("🍱 점심 메뉴들을 쉼표(,)로 입력해주세요:", ", ".join(default_menu))
menu_list = [m.strip() for m in menus.split(",") if m.strip()]

if "angle" not in st.session_state:
    st.session_state.angle = 0
if "selected_index" not in st.session_state:
    st.session_state.selected_index = None
if "spinning" not in st.session_state:
    st.session_state.spinning = False

def draw_wheel(menu_list, angle_deg):
    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw={'projection': 'polar'})
    num = len(menu_list)
    colors = plt.cm.tab20.colors
    wedges = np.ones(num)
    angles = np.linspace(0, 2 * np.pi, num + 1)
    labels = menu_list

    bars = ax.bar(
        x=angles[:-1],
        height=np.ones(num),
        width=2 * np.pi / num,
        bottom=0.0,
        color=[colors[i % len(colors)] for i in range(num)],
        edgecolor='white',
        linewidth=2,
        align='edge'
    )

    for i, bar in enumerate(bars):
        angle = angles[i] + (np.pi / num)
        ax.text(angle, 0.5, labels[i], rotation=angle * 180 / np.pi, rotation_mode='anchor',
                ha='center', va='center', fontsize=10, color='white', weight='bold')

    ax.set_theta_offset(np.deg2rad(angle_deg))
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.set_ylim(0, 1)

    return fig

def spin_wheel():
    st.session_state.spinning = True
    total_rotation = random.randint(360 * 5, 360 * 8)
    deceleration = 0.97
    speed = 20
    angle = st.session_state.angle

    placeholder = st.empty()

    while speed > 0.1:
        angle += speed
        angle = angle % 360
        fig = draw_wheel(menu_list, angle)
        placeholder.pyplot(fig)
        time.sleep(0.05)
        speed *= deceleration

    slice_angle = 360 / len(menu_list)
    selected_index = int(((360 - angle) % 360) // slice_angle)
    st.session_state.selected_index = selected_index
    st.session_state.angle = angle
    st.session_state.spinning = False

# 룰렛 그리기
st.subheader("🎡 룰렛")
fig = draw_wheel(menu_list, st.session_state.angle)
st.pyplot(fig)

if st.button("🍽️ 점심 메뉴 뽑기!", disabled=st.session_state.spinning):
    spin_wheel()

if st.session_state.selected_index is not None:
    st.success(f"오늘의 점심은... **{menu_list[st.session_state.selected_index]}** 입니다! 🎉")
