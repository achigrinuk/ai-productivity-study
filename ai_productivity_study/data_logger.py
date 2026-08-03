import pandas as pd
import uuid
from datetime import datetime

class DataLogger:
    def __init__(self, csv_file_path="data/results.csv"):
        self.csv_file_path = csv_file_path
        self._initialize_csv()

    def _initialize_csv(self):
        try:
            pd.read_csv(self.csv_file_path)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            df = pd.DataFrame(columns=[
                'participant_id', 'timestamp', 'trial_number', 'condition',
                'puzzle_type', 'time_taken', 'correct_answer',
                'hints_used', 'has_ai_assistance', 'response_correct'
            ])
            df.to_csv(self.csv_file_path, index=False)

    def log_trial(self, participant_id, trial_number, condition, puzzle_type,
                  time_taken, correct_answer, hints_used, has_ai_assistance, response_correct):
        timestamp = datetime.now().isoformat()

        new_row = pd.DataFrame({
            'participant_id': [participant_id],
            'timestamp': [timestamp],
            'trial_number': [trial_number],
            'condition': [condition],
            'puzzle_type': [puzzle_type],
            'time_taken': [time_taken],
            'correct_answer': [correct_answer],
            'hints_used': [hints_used],
            'has_ai_assistance': [has_ai_assistance],
            'response_correct': [response_correct]
        })

        new_row.to_csv(self.csv_file_path, mode='a', header=False, index=False)

        return timestamp

def create_results_file(file_path="data/results.csv"):
    df = pd.DataFrame(columns=[
        'participant_id', 'timestamp', 'trial_number', 'condition',
        'puzzle_type', 'time_taken', 'correct_answer',
        'hints_used', 'has_ai_assistance', 'response_correct'
    ])
    df.to_csv(file_path, index=False)
    return DataLogger(file_path)