import os
import pandas as pd
import streamlit as st

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
        """Ensures the local CSV file exists with proper column headers."""
        if not os.path.exists(self.filename):
            df = pd.DataFrame(columns=self.fieldnames)
            df.to_csv(self.filename, index=False)

    def log_trial(self, **kwargs):
        """
        Logs trial data locally to CSV and attempts to sync directly
        to Google Sheets using Streamlit's GSheetsConnection.
        """
        # 1. Local CSV Backup Logging (Always works offline)
        try:
            df_new = pd.DataFrame([kwargs])
            df_new.to_csv(
                self.filename, 
                mode='a', 
                header=not os.path.exists(self.filename), 
                index=False
            )
        except Exception as e:
            st.warning(f"Local CSV logging warning: {e}")

        # 2. Cloud Google Sheets Logging
        try:
            from streamlit_gsheets import GSheetsConnection
            
            # Establish connection using [connections.gsheets] from secrets
            conn = st.connection("gsheets", type=GSheetsConnection)
            
            # Read existing sheet data
            existing_df = conn.read(ttl=0) # ttl=0 ensures fresh data read
            
            # Append new record row
            updated_df = pd.concat([existing_df, pd.DataFrame([kwargs])], ignore_index=True)
            
            # Update Google Sheet
            conn.update(data=updated_df)
        except Exception as cloud_err:
            # If secrets are missing or network drops, local CSV backup handles it
            pass

    def get_all_data(self):
        """Retrieves full historical dataset from local CSV."""
        if os.path.exists(self.filename):
            return pd.read_csv(self.filename)
        return pd.DataFrame(columns=self.fieldnames)
