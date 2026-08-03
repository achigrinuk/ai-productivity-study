import streamlit as st
import time
import uuid
import json
import random
from game_logic import PuzzleGenerator, AIAssistant, run_trial
from data_logger import DataLogger

# Page configuration
st.set_page_config(
    page_title="AI Productivity Research Study",
    page_icon="🧠",
    layout="centered",
)

# Initialize session state
def init_session_state():
    if 'participant_id' not in st.session_state:
        st.session_state.participant_id = str(uuid.uuid4())[:8]
    if 'current_trial' not in st.session_state:
        st.session_state.current_trial = 0
    if 'total_trials' not in st.session_state:
        st.session_state.total_trials = 0
    if 'results' not in st.session_state:
        st.session_state.results = []
    if 'game_active' not in st.session_state:
        st.session_state.game_active = False
    if 'puzzle' not in st.session_state:
        st.session_state.puzzle = None
    if 'condition' not in st.session_state:
        st.session_state.condition = None
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'hints_used' not in st.session_state:
        st.session_state.hints_used = 0
    if 'ai_assistant' not in st.session_state:
        st.session_state.ai_assistant = AIAssistant()
    if 'puzzle_gen' not in st.session_state:
        st.session_state.puzzle_gen = PuzzleGenerator()
    if 'show_results' not in st.session_state:
        st.session_state.show_results = False
    if 'phase' not in st.session_state:
        st.session_state.phase = 'consent'


def show_consent():
    """Display consent form and begin the study."""
    st.header("🧠 AI Productivity Research Study")
    st.markdown("### Informed Consent")

    st.markdown("""
    **Purpose of this Study**

    This research study investigates how AI assistance affects human task productivity and accuracy.
    You will complete a series of puzzles, some with AI assistance and some without.

    **What you will do:**
    - Complete 10 puzzle trials
    - Some trials will have AI assistance (hints or answers)
    - Some trials will have no assistance
    - Each puzzle is timed for accuracy and speed measurement

    **Your Rights:**
    - Participation is voluntary
    - You may stop at any time without penalty
    - Your data is anonymous and identified only by a random ID
    - Results are used for research purposes only

    **Duration:** Approximately 10-15 minutes
    """)

    consent = st.checkbox("I consent to participate in this study", key='consent_checkbox')

    if consent:
        if st.button("Begin Study", type='primary'):
            st.session_state.phase = 'instructions'
            st.rerun()


def show_instructions():
    """Display study instructions."""
    st.header("📋 Study Instructions")

    st.markdown("""
    **How the study works:**

    1. You will see a series of **puzzles** one at a time
    2. Each puzzle has a **time limit** — solve it as quickly and accurately as possible
    3. Some puzzles will have an **AI Assistant** available (a button will appear)
    4. Other puzzles will have **no assistance** — solve them on your own
    5. After each puzzle, you'll see if your answer was correct
    6. Try your best on every puzzle!

    **Tips:**
    - Don't spend too long on any single puzzle
    - Use the AI assistant wisely when it's available
    - Your speed and accuracy both matter
    """)

    if st.button("Start Trials", type='primary'):
        st.session_state.total_trials = 10
        st.session_state.current_trial = 0
        st.session_state.phase = 'trial'
        st.session_state.game_active = True
        st.rerun()


def next_trial():
    """Advance to the next trial or end the study."""
    st.session_state.current_trial += 1

    if st.session_state.current_trial >= st.session_state.total_trials:
        st.session_state.phase = 'results'
        st.session_state.show_results = True
    else:
        st.session_state.puzzle = None
        st.session_state.condition = None
        st.session_state.hints_used = 0
        st.rerun()


def run_single_trial():
    """Run a single trial of the experiment."""
    trial_num = st.session_state.current_trial + 1
    total = st.session_state.total_trials

    st.markdown(f"### Trial {trial_num} of {total}")

    # Progress bar
    progress = st.session_state.current_trial / st.session_state.total_trials
    st.progress(progress)

    # Determine condition (AI vs No-AI) - random assignment
    if st.session_state.condition is None:
        st.session_state.condition = random.choice(['AI', 'No-AI'])

    # Show condition indicator
    if st.session_state.condition == 'AI':
        st.info("🤖 **AI Assistance: AVAILABLE** — You can use the hint/answer button below")
    else:
        st.warning("🚫 **No AI Assistance** — Solve this puzzle on your own")

    # Generate puzzle if not already generated
    if st.session_state.puzzle is None:
        st.session_state.puzzle = st.session_state.puzzle_gen.generate_puzzle()

    puzzle = st.session_state.puzzle
    st.markdown(f"**{puzzle['question']}**")

    # Timer
    if st.session_state.start_time is None:
        st.session_state.start_time = time.time()

    elapsed = time.time() - st.session_state.start_time
    st.metric("⏱️ Time Elapsed", f"{elapsed:.1f}s")

    # AI Assistance button (only for AI condition)
    if st.session_state.condition == 'AI':
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💡 Get Hint", key='hint_btn'):
                hint = st.session_state.ai_assistant.provide_hint(puzzle, hint_level=1)
                st.session_state.hints_used += 1
                st.info(f"**Hint:** {hint}")
        with col2:
            if st.button("💡💡 Get Answer", key='answer_btn'):
                answer = st.session_state.ai_assistant.provide_answer(puzzle)
                st.session_state.hints_used += 1
                st.warning(f"**Answer:** {answer}")

    # User input
    user_answer = st.text_input("Your answer:", key='answer_input', placeholder="Type your answer here...")

    # Submit button
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Submit Answer", type='primary', key='submit_btn'):
            if user_answer.strip():
                is_correct, correct_solution = run_trial(puzzle, user_answer)
                time_taken = round(time.time() - st.session_state.start_time, 2)

                # Log the trial
                logger = DataLogger()
                logger.log_trial(
                    participant_id=st.session_state.participant_id,
                    trial_number=st.session_state.current_trial,
                    condition=st.session_state.condition,
                    puzzle_type=puzzle['type'],
                    time_taken=time_taken,
                    correct_answer=correct_solution,
                    hints_used=st.session_state.hints_used,
                    has_ai_assistance=(st.session_state.condition == 'AI'),
                    response_correct=is_correct
                )

                # Store result
                st.session_state.results.append({
                    'trial': st.session_state.current_trial,
                    'condition': st.session_state.condition,
                    'puzzle_type': puzzle['type'],
                    'time_taken': time_taken,
                    'correct': is_correct,
                    'hints_used': st.session_state.hints_used,
                    'user_answer': user_answer,
                    'correct_answer': correct_solution,
                })

                # Show feedback
                if is_correct:
                    st.success(f"✅ Correct! (Answer: {correct_solution})")
                else:
                    st.error(f"❌ Incorrect. The correct answer was: {correct_solution}")

                st.session_state.start_time = None
                st.session_state.puzzle = None
                st.session_state.condition = None
                st.session_state.hints_used = 0

                # Next trial after a brief pause
                time.sleep(1.5)
                next_trial()
            else:
                st.warning("Please enter an answer before submitting.")


def show_results():
    """Display final results."""
    st.header("📊 Study Complete!")
    st.markdown("Thank you for participating in the AI Productivity Research Study!")

    results = st.session_state.results

    if results:
        df = pd.DataFrame(results)

        st.subheader("Overall Performance")
        col1, col2, col3 = st.columns(3)
        with col1:
            accuracy = df['correct'].mean() * 100
            st.metric("Accuracy", f"{accuracy:.1f}%")
        with col2:
            avg_time = df['time_taken'].mean()
            st.metric("Avg Time per Trial", f"{avg_time:.1f}s")
        with col3:
            total_hints = df['hints_used'].sum()
            st.metric("Total Hints Used", total_hints)

        st.subheader("Performance by Condition")
        for condition in ['AI', 'No-AI']:
            subset = df[df['condition'] == condition]
            if len(subset) > 0:
                acc = subset['correct'].mean() * 100
                avg_t = subset['time_taken'].mean()
                st.markdown(f"**{condition}:** {acc:.1f}% accuracy, {avg_t:.1f}s avg time")

        st.subheader("Detailed Results")
        st.dataframe(df[['trial', 'condition', 'puzzle_type', 'time_taken', 'correct', 'hints_used']])

        # Save summary
        st.download_button(
            label="📥 Download Results (CSV)",
            data=df.to_csv(index=False),
            file_name=f"study_results_{st.session_state.participant_id}.csv",
            mime="text/csv"
        )

    if st.button("🔄 Start New Study", key='restart_btn'):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        init_session_state()
        st.rerun()


def main():
    init_session_state()

    st.markdown("---")

    if st.session_state.phase == 'consent':
        show_consent()
    elif st.session_state.phase == 'instructions':
        show_instructions()
    elif st.session_state.phase == 'trial' and st.session_state.game_active:
        if st.session_state.current_trial < st.session_state.total_trials:
            run_single_trial()
        else:
            show_results()
    elif st.session_state.phase == 'results' or st.session_state.show_results:
        show_results()

    # Sidebar with participant info
    with st.sidebar:
        st.markdown("### Participant Info")
        st.markdown(f"**ID:** {st.session_state.participant_id}")
        st.markdown(f"**Phase:** {st.session_state.phase}")
        if st.session_state.get('current_trial') is not None:
            st.markdown(f"**Trial:** {st.session_state.current_trial + 1}/{st.session_state.total_trials}")


if __name__ == "__main__":
    main()
