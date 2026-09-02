import streamlit as st
import time
import uuid
import random
import pandas as pd
from game_logic import generate_puzzle, check_answer
from data_logger import DataLogger

# Page configuration
st.set_page_config(
    page_title="AI Productivity & Cognition Study",
    page_icon="🧠",
    layout="centered"
)

logger = DataLogger()

# Initialize session state variables
defaults = {
    'phase': 'consent',
    'participant_id': "",
    'current_trial': 0,
    'total_trials': 10,
    'results': [],
    'game_active': False,
    'current_puzzle': None,
    'puzzle_start_time': 0,
    'hint_click_time': None,
    'hints_used': 0,
    'show_hint': False,
    'used_puzzles': []
}

for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

def show_consent():
    st.title("🧠 Research Study: Human Decision-Making & AI Assistance")
    st.write("""
    ### Welcome!
    You are participating in an empirical study measuring problem-solving efficiency and verification when utilizing AI assistance.
    
    **What you will do:**
    - Complete **10 problem-solving tasks**.
    - Some tasks offer **AI Assistance**.
    - Your speed, accuracy, and confidence will be recorded anonymously.
    
    **Time required:** ~5-8 minutes.
    """)
    
    participant_input = st.text_input("Enter Participant ID (or leave blank to auto-generate):")
    
    if st.button("I Agree & Start Study", type="primary"):
        if participant_input.strip():
            st.session_state.participant_id = participant_input.strip()
        else:
            st.session_state.participant_id = f"P_{str(uuid.uuid4())[:8]}"
        st.session_state.phase = 'instructions'
        st.rerun()

def show_instructions():
    st.title("Instructions")
    st.write(f"**Participant ID:** `{st.session_state.participant_id}`")
    st.write("""
    1. Answer as **accurately and quickly** as possible.
    2. On trials with **AI Assistance Available**, you may choose whether to click for a hint.
    3. Rate your confidence level after submitting each answer.
    """)
    if st.button("Begin Study", type="primary"):
        st.session_state.phase = 'trial'
        st.session_state.current_trial = 1
        st.session_state.game_active = True
        st.session_state.used_puzzles = []
        st.rerun()

def run_single_trial():
    trial_num = st.session_state.current_trial
    st.subheader(f"Trial {trial_num} of {st.session_state.total_trials}")
    
    if st.session_state.current_puzzle is None:
        has_ai = random.choice([True, False])
        condition = "AI" if has_ai else "No-AI"
        
        puzzle = generate_puzzle(exclude_list=st.session_state.used_puzzles)
        st.session_state.current_puzzle = {
            'puzzle': puzzle,
            'condition': condition,
            'has_ai': has_ai
        }
        st.session_state.used_puzzles.append(puzzle['id'])
        st.session_state.puzzle_start_time = time.time()
        st.session_state.hint_click_time = None
        st.session_state.hints_used = 0
        st.session_state.show_hint = False

    current = st.session_state.current_puzzle
    puzzle = current['puzzle']
    
    st.caption(f"Category: {puzzle['complexity']} | Type: {puzzle['type']}")
    st.markdown(f"### Question:\n{puzzle['question']}")
    
    # AI Hint Interface
    if current['has_ai']:
        st.info("💡 **AI Assistance Available**")
        if not st.session_state.show_hint:
            if st.button("Get AI Hint"):
                st.session_state.show_hint = True
                st.session_state.hints_used += 1
                st.session_state.hint_click_time = time.time()
                st.rerun()
        else:
            st.warning(f"🤖 **AI Output:** {puzzle['selected_hint']}")
            
    # Submission Form
    with st.form(key=f"trial_form_{trial_num}"):
        user_answer = st.text_input("Your Answer:")
        confidence = st.slider("How confident are you in this answer?", 1, 5, 3, 
                               help="1 = Guessing, 5 = Completely Certain")
        submitted = st.form_submit_button("Submit Answer")
        
        if submitted:
            end_time = time.time()
            total_time = round(end_time - st.session_state.puzzle_start_time, 2)
            time_to_hint = round(st.session_state.hint_click_time - st.session_state.puzzle_start_time, 2) if st.session_state.hint_click_time else None
            
            is_correct = check_answer(user_answer, puzzle['answer'])
            
            trial_data = {
                "participant_id": st.session_state.participant_id,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "trial_number": trial_num,
                "condition": current['condition'],
                "puzzle_type": puzzle['type'],
                "complexity": puzzle['complexity'],
                "time_taken": total_time,
                "time_to_hint": time_to_hint,
                "correct_answer": str(puzzle['answer']),
                "user_answer": str(user_answer),
                "hints_used": st.session_state.hints_used,
                "has_ai_assistance": current['has_ai'],
                "is_hallucinated": puzzle.get('is_hallucinated', False) if current['has_ai'] and st.session_state.show_hint else False,
                "confidence_level": confidence,
                "response_correct": is_correct
            }
            
            logger.log_trial(**trial_data)
            st.session_state.results.append(trial_data)
            
            if is_correct:
                st.success(f"Correct! ({total_time}s)")
            else:
                st.error(f"Incorrect. Correct answer: {puzzle['answer']}")
                
            time.sleep(1.0)
            
            st.session_state.current_puzzle = None
            if st.session_state.current_trial < st.session_state.total_trials:
                st.session_state.current_trial += 1
            else:
                st.session_state.phase = 'results'
            st.rerun()

def show_results():
    st.title("🎉 Study Completed")
    st.write(f"Participant ID: `{st.session_state.participant_id}`")
    
    results = st.session_state.results
    if results:
        df = pd.DataFrame(results)
        
        st.subheader("Performance Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Accuracy", f"{int(df['response_correct'].mean() * 100)}%")
        col2.metric("Avg Time", f"{round(df['time_taken'].mean(), 1)}s")
        col3.metric("Avg Confidence", f"{round(df['confidence_level'].mean(), 1)}/5")
        
        st.dataframe(df[['trial_number', 'condition', 'complexity', 'time_taken', 'confidence_level', 'response_correct']])
        
        csv_data = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Session Results (CSV)",
            data=csv_data,
            file_name=f"results_{st.session_state.participant_id}.csv",
            mime="text/csv"
        )

    st.markdown("---")
    with st.expander("🔐 Admin Data Export (Researcher Only)"):
        admin_pass = st.text_input("Enter Admin Password:", type="password")
        if admin_pass == "stir2026":
            all_data = logger.get_all_data()
            if not all_data.empty:
                st.write(f"**Total Records Logged:** {len(all_data)}")
                st.dataframe(all_data.tail(10))
                st.download_button(
                    label="📥 Download Full Dataset (All Participants)",
                    data=all_data.to_csv(index=False),
                    file_name="full_study_results.csv",
                    mime="text/csv"
                )
            else:
                st.info("No participant records logged on this container instance yet.")
        elif admin_pass:
            st.error("Incorrect password.")
        
    if st.button("Start New Session"):
        st.session_state.phase = 'consent'
        st.session_state.results = []
        st.session_state.current_trial = 0
        st.session_state.current_puzzle = None
        st.rerun()

def main():
    if st.session_state.phase == 'consent':
        show_consent()
    elif st.session_state.phase == 'instructions':
        show_instructions()
    elif st.session_state.phase == 'trial':
        run_single_trial()
    elif st.session_state.phase == 'results':
        show_results()

if __name__ == "__main__":
    main()
