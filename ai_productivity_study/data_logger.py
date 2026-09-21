import pandas as pd
import os
import streamlit as st
from datetime import datetime

class DataLogger:
    def __init__(self, filename="study_data.csv"):
        self.filename = filename
        self.fieldnames = [
            "participant_id", "timestamp", "trial_number", "condition",
            "puzzle_type", "complexity", "time_taken", "time_to_hint",
            "correct_answer", "user_answer", "hints_used",
            "has_ai_assistance", "is_hallucinated", "confidence_level",
            "response_correct"
        ]
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.filename):
            df = pd.DataFrame(columns=self.fieldnames)
            df.to_csv(self.filename, index=False)

    def log_trial(self, **kwargs):
        # 1. Local CSV Backup Logging
        try:
            df_new = pd.DataFrame([kwargs])
            df_new.to_csv(self.filename, mode='a', header=not os.path.exists(self.filename), index=False)
        except Exception as e:
            st.warning(f"Local CSV logging warning: {e}")

        # 2. Cloud Google Sheets Logging (if Streamlit Cloud secrets configured)
        try:
            if "gsheets" in st.secrets:
                from streamlit_gsheets import GSheetsConnection
                conn = st.connection("gsheets", type=GSheetsConnection)
                existing_df = conn.read()
                updated_df = pd.concat([existing_df, pd.DataFrame([kwargs])], ignore_index=False)
                conn.update(data=updated_df)
        except Exception as cloud_err:
            # Silent fallback to local storage if internet drops during live testing
            pass

    def get_all_data(self):
        if os.path.exists(self.filename):
            return pd.read_csv(self.filename)
        return pd.DataFrame(columns=self.fieldnames)
