import os
import pandas as pd
from pathlib import Path

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
                "puzzle_type", "complexity", "time_taken", "correct_answer", 
                "user_answer", "hints_used", "has_ai_assistance", 
                "is_hallucinated", "confidence_level", "response_correct"
            ])
            df.to_csv(self.csv_file_path, index=False)

    def log_trial(self, **kwargs):
        os.makedirs(self.csv_file_path.parent, exist_ok=True)
        
        if len(kwargs) == 1 and isinstance(next(iter(kwargs.values())), dict):
            data = next(iter(kwargs.values()))
        else:
            data = kwargs

        df_new = pd.DataFrame([data])
        if self.csv_file_path.exists():
            df_existing = pd.read_csv(self.csv_file_path)
            df_updated = pd.concat([df_existing, df_new], ignore_index=True)
            df_updated.to_csv(self.csv_file_path, index=False)
        else:
            df_new.to_csv(self.csv_file_path, index=False)

    def get_all_data(self):
        """Returns all collected research data as a DataFrame."""
        if self.csv_file_path.exists():
            try:
                return pd.read_csv(self.csv_file_path)
            except Exception:
                return pd.DataFrame()
        return pd.DataFrame()
