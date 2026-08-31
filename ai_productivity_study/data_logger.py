import os
import pandas as pd
from pathlib import Path

class DataLogger:
    def __init__(self, csv_file_path=None):
        # Resolve absolute path relative to this file's directory
        if csv_file_path is None:
            base_dir = Path(__file__).resolve().parent
            self.csv_file_path = base_dir / "data" / "results.csv"
        else:
            self.csv_file_path = Path(csv_file_path).resolve()
            
        self._initialize_csv()

    def _initialize_csv(self):
        # Guarantee parent folder exists
        os.makedirs(self.csv_file_path.parent, exist_ok=True)
            
        # Create empty CSV with headers if it doesn't exist yet
        if not self.csv_file_path.exists():
            df = pd.DataFrame(columns=[
                "participant_id", "timestamp", "trial_number", "condition", 
                "puzzle_type", "time_taken", "correct_answer", "hints_used", 
                "has_ai_assistance", "response_correct"
            ])
            df.to_csv(self.csv_file_path, index=False)

    def log_trial(self, data_dict):
        # Guarantee folder exists before append
        os.makedirs(self.csv_file_path.parent, exist_ok=True)
        
        if not self.csv_file_path.exists():
            self._initialize_csv()
            
        df = pd.DataFrame([data_dict])
        df.to_csv(self.csv_file_path, mode='a', header=False, index=False)
