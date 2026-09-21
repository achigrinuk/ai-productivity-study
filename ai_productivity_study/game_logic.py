import random

PUZZLE_BANK = [
    {
        "id": 1,
        "type": "CRT",
        "complexity": "Medium",
        "question": "A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost in cents?",
        "answer": ["5", "5 cents", "0.05", "$0.05"],
        "accurate_hint": "Break down the algebra: Let ball = x. Bat = x + 1.00. Total: x + (x + 1.00) = 1.10. Solve for 2x = 0.10.",
        "flawed_hint": "Since the total is $1.10 and the bat is $1.00 more, simply subtract $1.00 from $1.10 to get $0.10 (10 cents)."
    },
    {
        "id": 2,
        "type": "Logic",
        "complexity": "Hard",
        "question": "If 5 machines take 5 minutes to make 5 widgets, how many minutes does it take 100 machines to make 100 widgets?",
        "answer": ["5", "5 minutes", "5 min"],
        "accurate_hint": "Look at the rate per machine: 1 machine takes 5 minutes to make 1 widget. Thus, 100 machines working simultaneously still need 5 minutes.",
        "flawed_hint": "Set up a direct proportion: 5 machines/5 mins = 100 machines/x mins. Scaling up 20x means it takes 100 minutes."
    },
    {
        "id": 3,
        "type": "Spatial",
        "complexity": "Easy",
        "question": "In a lake, there is a patch of lily pads. Every day, the patch doubles in size. If it takes 48 days to cover the entire lake, how many days does it take to cover half the lake?",
        "answer": ["47", "47 days"],
        "accurate_hint": "Work backward from day 48: Since it doubles every day, the lake was half covered exactly one day before day 48.",
        "flawed_hint": "Divide the total time by 2: Since half the lake needs to be covered, 48 days / 2 = 24 days."
    },
    {
        "id": 4,
        "type": "Numerical",
        "complexity": "Medium",
        "question": "What is the next number in the sequence: 2, 4, 8, 16, 32, __?",
        "answer": ["64"],
        "accurate_hint": "Each number doubles the previous term (multiply by 2 each step). 32 * 2 = 64.",
        "flawed_hint": "Notice the sequence pattern increases exponentially by adding powers of 10: 32 + 30 = 62."
    }
]

def generate_puzzle(exclude_list=None):
    if exclude_list is None:
        exclude_list = []
    
    available_puzzles = [p for p in PUZZLE_BANK if p["id"] not in exclude_list]
    
    # Reset pool if all puzzles have been used in this session
    if not available_puzzles:
        available_puzzles = PUZZLE_BANK.copy()
        
    selected = random.choice(available_puzzles).copy()
    
    # 50/50 chance to serve accurate vs flawed hint when AI hint is requested
    is_hallucinated = random.choice([True, False])
    selected['selected_hint'] = selected['flawed_hint'] if is_hallucinated else selected['accurate_hint']
    selected['is_hallucinated'] = is_hallucinated
    
    return selected

def check_answer(user_input, correct_answers):
    if not user_input:
        return False
    cleaned_input = str(user_input).strip().lower()
    acceptable = [str(ans).strip().lower() for ans in correct_answers] if isinstance(correct_answers, list) else [str(correct_answers).strip().lower()]
    return cleaned_input in acceptable
