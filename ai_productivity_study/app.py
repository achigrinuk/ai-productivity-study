import streamlit as st
import time
import uuid
import json
import random
import pandas as pd
from game_logic import generate_puzzle, check_answer
from data_logger import DataLogger

# Page configuration
st.set_page_config(
    page_title="AI Productivity Study",
    page_icon="🧠",
    layout="centered"
)

# Initialize logger
logger = DataLogger()

# Initialize session state
if 'phase' not in st.session_state:
    st.session_state.phase = 'consent'
if 'participant_id' not in st.session_state:
    st.session_state.participant_id = ""
if 'current_trial' not in st.session_state:
    st.session_state.current_trial = 0
if 'total_trials' not in st.session_state:
    st.session_state.total_trials = 10
if 'results' not in st.session_state:
    st.session_state.results = []
if 'game_active' not in st.session_state:
    st.session_state.game_active = False
if 'current_puzzle' not in st.session_state:
    st.session_state.current_puzzle = None
if 'puzzle_start_time' not in st.session_state:
    st.session_state.puzzle_start_time = 0
if 'hints_used' not in st.session_state:
    st.session_state.hints_used = 0
if 'show_hint' not in st.session_state:
    st.session_state.show_hint = False
if 'used_puzzles' not in st.session_state:
    st.session_state.used_puzzles = []

def show_consent():
    st.title("🧠 Research Study: Problem Solving & Assistance")
    st.write("""
    ### Welcome!
    You are invited to participate in a research study investigating problem-solving efficiency.
    
    **What you will do:**
    - Complete 10 short logic and math puzzles.
    - Some puzzles may provide AI-generated hints or assistance.
    - Your accuracy and completion time will be recorded anonymously.
    
    **Time required:** ~5-10 minutes.
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
    1. You will solve **10 short puzzles**.
    2. Try to answer as quickly and accurately as possible.
    3. On half of the trials, you will have access to an **AI Hint**.
    4. Click **Submit Answer** when you are ready.
    """)
    if st.button("Begin Puzzles", type="primary"):
        st.session_state.phase = 'trial'
        st.session_state.current_trial = 1
        st.session_state.game_active = True
        st.session_state.used_puzzles = []
        st.rerun()

def run_single_trial():
    trial_num = st.session_state.current_trial
    st.subheader(f"Trial {trial_num} of {st.session_state.total_trials}")
    
    # Generate puzzle once per trial
    if st.session_state.current_puzzle is None:
        has_ai = random.choice([True, False])
        condition = "AI" if has_ai else "No-AI"
        
        puzzle = generate_puzzle(exclude_list=st.session_state.used_puzzles)
        st.session_state.current_puzzle = {
            'puzzle': puzzle,
            'condition': condition,
            'has_ai': has_ai
        }
        # Track unique puzzle ID to prevent repetition
        st.session_state.used_puzzles.append(puzzle['id'])
        st.session_state.puzzle_start_time = time.time()
        st.session_state.hints_used = 0
        st.session_state.show_hint = False

    current = st.session_state.current_puzzle
    puzzle = current['puzzle']
    
    # Display puzzle
    st.markdown(f"**Question:** {puzzle['question']}")
    
    # AI Assistance UI
    if current['has_ai']:
        st.info("💡 **AI Assistance Available for this trial!**")
        if not st.session_state.show_hint:
            if st.button("Get AI Hint"):
                st.session_state.show_hint = True
                st.session_state.hints_used += 1
                st.rerun()
        else:
            st.warning(f"🤖 **AI Hint:** {puzzle['hint']}")
            
    # User Response Form
    with st.form(key=f"trial_form_{trial_num}"):
        user_answer = st.text_input("Your Answer:")
        submitted = st.form_submit_button("Submit Answer")
        
        if submitted:
            time_taken = round(time.time() - st.puzzle_start_time if hasattr(st, 'puzzle_start_time') else time.time() - st.session_state.puzzle_start_time, 2)
            is_correct = check_answer(user_answer, puzzle['answer'])
            
            trial_data = {
                "participant_id": st.session_state.participant_id,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "trial_number": trial_num,
                "condition": current['condition'],
                "puzzle_type": puzzle['type'],
                "time_taken": time_taken,
                "correct_answer": str(puzzle['answer']),
                "user_answer": str(user_answer),
                "hints_used": st.session_state.hints_used,
                "has_ai_assistance": current['has_ai'],
                "response_correct": is_correct
            }
            
            # Save data locally on server
            logger.log_trial(**trial_data)
            st.session_state.results.append(trial_data)
            
            if is_correct:
                st.success(f"Correct! ({time_taken}s)")
            else:
                st.error(f"Incorrect. The correct answer was: {puzzle['answer']}")
                
            time.sleep(1.0)
            
            # Advance trial
            st.session_state.current_puzzle = None
            if st.session_state.current_trial < st.session_state.total_trials:
                st.session_state.current_trial += 1
            else:
                st.session_state.phase = 'results'
            st.rerun()

def show_results():
    st.title("🎉 Study Completed!")
    st.write(f"Thank you for participating! Participant ID: `{st.session_state.participant_id}`")
    
    results = st.session_state.results
    if results:
        df = pd.DataFrame(results)
        
        st.subheader("Summary Performance")
        col1, col2, col3 = st.columns(3)
        col1.metric("Accuracy", f"{int(df['response_correct'].mean() * 100)}%")
        col2.metric("Avg Time / Puzzle", f"{round(df['time_taken'].mean(), 1)}s")
        col3.metric("Total Puzzles", len(df))
        
        st.dataframe(df[['trial_number', 'condition', 'puzzle_type', 'time_taken', 'response_correct']])
        
        # Immediate participant download
        csv_data = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Session Results (CSV)",
            data=csv_data,
            file_name=f"results_{st.session_state.participant_id}.csv",
            mime="text/csv"
        )

    # Secret Admin Data Retrieval Portal
    st.markdown("---")
    with st.expander("🔐 Admin Data Export (Researcher Only)"):
        admin_pass = st.text_input("Enter Admin Password:", type="password")
        if admin_pass == "stir2026":  # You can change this password
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
                st.info("No participant records logged yet.")
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
