import os
import pandas as pd
from pathlib import Path
import streamlit as st
from streamlit_gsheets import GSheetsConnection

class DataLogger:
    def __init__(self, csv_file_path=None):
        if csv_file_path is None:
            base_dir = Path(__file__).resolve().parent
            self.csv_file_path = base_dir / "data" / "results.csv"
        else:
            self.csv_file_path = Path(csv_file_path).resolve()
            
        self._initialize_csv()

    def _initialize_csv(self):
        os.makedirs(self.csv_file_path.parent, exist_ok=True)
        if not self.csv_file_path.exists():
            df = pd.DataFrame(columns=[
                "participant_id", "timestamp", "trial_number", "condition", 
                "puzzle_type", "complexity", "time_taken", "time_to_hint",
                "correct_answer", "user_answer", "hints_used", "has_ai_assistance", 
                "is_hallucinated", "confidence_level", "response_correct"
            ])
            df.to_csv(self.csv_file_path, index=False)

    def log_trial(self, **kwargs):
        # 1. Format the new trial data into a DataFrame row
        if len(kwargs) == 1 and isinstance(next(iter(kwargs.values())), dict):
            data = next(iter(kwargs.values()))
        else:
            data = kwargs

        df_new = pd.DataFrame([data])

        # 2. Append to Google Sheets (Primary cloud storage)
        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            existing_data = conn.read(ttl=0) # Read current live data without caching
            
            if existing_data.empty:
                updated_df = df_new
            else:
                updated_df = pd.concat([existing_data, df_new], ignore_index=True)
                
            conn.update(data=updated_df)
        except Exception as e:
            st.warning(f"Note: Could not sync to Google Sheets ({e}). Saved locally.")

        # 3. Append to local CSV (Fallback storage)
        os.makedirs(self.csv_file_path.parent, exist_ok=True)
        if self.csv_file_path.exists():
            df_existing = pd.read_csv(self.csv_file_path)
            df_updated = pd.concat([df_existing, df_new], ignore_index=True)
            df_updated.to_csv(self.csv_file_path, index=False)
        else:
            df_new.to_csv(self.csv_file_path, index=False)

    def get_all_data(self):
        """Fetches all collected data directly from Google Sheets if available, else local CSV."""
        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            sheet_data = conn.read(ttl=0)
            if not sheet_data.empty:
                return sheet_data
        except Exception:
            pass

        if self.csv_file_path.exists():
            try:
                return pd.read_csv(self.csv_file_path)
            except Exception:
                return pd.DataFrame()
        return pd.DataFrame()
