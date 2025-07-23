# (기존 코드까지 유지하고 그 아래에 이어서 추가하세요)

# --- 💡 성적 향상 시뮬레이션 기능 ---
st.subheader("📈 시뮬레이션: 성적 향상 시 진학 가능 대학 변화")

# 평균 등급 변화 시뮬레이션 함수
def simulate_avg_with_improved_grade(target_subj, new_grade):
    temp_score = 0
    for subj in st.session_state.subjects:
        name = subj["name"]
        unit = subj["unit"]
        if name == target_subj:
            score = grade_score[new_grade]
        else:
            score = grade_score[subj["grade"]]
        temp_score += score * unit
    return round(temp_score / total_units, 2)

# 대학 예측 함수 재사용
def predict_university(avg):
    if avg <= 1.10:
        return "🏆 의대, 치대, 한의대, 약대, 수의대, SKY(서울대/연세대/고려대)"
    elif avg <= 1.20:
        return "🥇 서강대, 성균관대, 한양대(서울), 이화여대"
    elif avg <= 1.30:
        return "🎯 중경외시, 건국대(서울), 동국대, 홍익대, 서울시립대"
    elif avg <= 1.40:
        return "✅ 숙명여대, 서울여대, 세종대, 명지대, 가천대"
    elif avg <= 1.55:
        return "💡 숭실대, 단국대, 아주대, 광운대, 국민대, 상명대"
    elif avg <= 1.80:
        return "📘 서울과기대, 덕성여대, 한성대, 한신대, 서경대"
    elif avg <= 2.10:
        return "🔍 인하대, 인천대, 경기대, 가톨릭대 등 수도권 적성전형/논술 대학"
    elif avg <= 2.50:
        return "🏫 전북대, 전남대, 충남대, 경북대, 부경대 등 지방 거점 국립대"
    elif avg <= 3.20:
        return "🪴 대구대, 한남대, 우석대, 창원대, 계명대 등 지방 사립대"
    else:
        return "📉 전문대학 / 실기·특기자 / 직업계고 전형 추천"

# 성적 낮은 과목 상위 2개 추출
weak_subjects = sorted(subject_grades.items(), key=lambda x: -x[1])[:2]

for subj_name, current_score in weak_subjects:
    st.markdown(f"#### 🎯 `{subj_name}` (현재 {current_score}등급) → 향상 시뮬레이션")
    
    col1, col2 = st.columns(2)
    with col1:
        new_grade = st.selectbox(f"➡️ {subj_name}을(를) 몇 등급까지 올린다고 가정할까요?", 
                                 options=list(grade_score.keys()), 
                                 key=f"sim_{subj_name}")
    with col2:
        new_score = grade_score[new_grade]
        if new_score >= current_score:
            st.warning("등급을 향상된 수준으로 설정해주세요.")
            continue

    # 평균 등급 재계산
    new_avg = simulate_avg_with_improved_grade(subj_name, new_grade)
    current_univ = predict_university(avg_grade)
    new_univ = predict_university(new_avg)

    st.markdown(f"""
    ✅ 평균 등급 변화: **{avg_grade} → {new_avg} 등급**  
    🎓 대학 가능성:  
    - 기존: {current_univ}  
    - 향상 시: **{new_univ}**
    """)

    st.markdown("---")
