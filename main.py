    # --- 📈 시뮬레이션: 성적 향상 시 자동 등급별 변화 제안 ---
    st.subheader("📈 시뮬레이션: 성적 향상 시 진학 가능 대학 변화 (자동 제안)")

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

    for subj_name, current_score in weak_subjects:
        st.markdown(f"#### 🎯 `{subj_name}` (현재 {current_score}등급) → 등급별 시뮬레이션 결과")

        improved_levels = [g for g, s in grade_score.items() if s < current_score]
        for improved_grade in improved_levels:
            new_avg = simulate_avg_with_improved_grade(subj_name, improved_grade)
            new_univ = predict_university(new_avg)

            st.markdown(f"""
            🔹 `{subj_name}`을 **{improved_grade} 등급**까지 올릴 경우:  
            → 평균 등급 **{new_avg}**, 진학 가능 대학군 👉 **{new_univ}**
            """)

        st.markdown("---")
