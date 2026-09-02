import random

RAW_PUZZLE_BANK = [
    {"id": "scramble_coding", "question_type": "scramble", "word": "coding", "hint": "It's what software engineers do.", "type": "scramble"},
    {"id": "scramble_python", "question_type": "scramble", "word": "python", "hint": "A popular programming language named after a snake.", "type": "scramble"},
    {"id": "scramble_algorithm", "question_type": "scramble", "word": "algorithm", "hint": "A set of rules to solve a problem in computer science.", "type": "scramble"},
    {"id": "seq_2_4_8", "question": "What comes next in the sequence: 2, 4, 8, 16, ___?", "answer": "32", "hint": "Each number doubles the previous number.", "type": "pattern"},
    {"id": "logic_workers", "question": "If 5 workers build 5 tables in 5 hours, how many hours does 1 worker take to build 1 table?", "answer": "5", "hint": "Think about individual worker rate.", "type": "logic"},
    {"id": "math_15_12", "question": "What is 15 x 12?", "answer": "180", "hint": "15 x 10 = 150, then add 15 x 2.", "type": "math"},
    {"id": "seq_3_6_12", "question": "What comes next in the sequence: 3, 6, 12, 24, ___?", "answer": "48", "hint": "Multiply by 2 each step.", "type": "pattern"},
    {"id": "logic_feathers", "question": "Which is heavier: a pound of feathers or a pound of bricks?", "answer": "neither", "hint": "Pay close attention to the units of weight.", "type": "logic"},
    {"id": "math_144_12", "question": "What is 144 / 12?", "answer": "12", "hint": "12 squared equals 144.", "type": "math"},
    {"id": "seq_fibonacci", "question": "What comes next: 1, 1, 2, 3, 5, 8, ___?", "answer": "13", "hint": "Add the two previous numbers (Fibonacci sequence).", "type": "pattern"},
    {"id": "logic_bat_ball", "question": "A bat and ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much is the ball in cents?", "answer": "5", "hint": "Let ball = x, bat = x + 1.00. 2x + 1.00 = 1.10.", "type": "logic"},
    {"id": "math_25_4_15", "question": "What is 25 x 4 - 15?", "answer": "85", "hint": "Multiply 25 by 4 first, then subtract 15.", "type": "math"}
]

def scramble_word(word):
    """Takes a word and randomly shuffles its letters."""
    chars = list(word.upper())
    while True:
        random.shuffle(chars)
        scrambled = " ".join(chars)
        if scrambled != " ".join(list(word.upper())):
            return scrambled

def generate_puzzle(exclude_list=None):
    if exclude_list is None:
        exclude_list = []
        
    # Exclude puzzles whose unique 'id' is already in the used list
    available = [p for p in RAW_PUZZLE_BANK if p['id'] not in exclude_list]
    if not available:
        available = RAW_PUZZLE_BANK
        
    selected = random.choice(available).copy()
    
    if selected.get('question_type') == 'scramble':
        target_word = selected['word']
        scrambled_str = scramble_word(target_word)
        selected['question'] = f"Unscramble this word: '{scrambled_str}'"
        selected['answer'] = target_word
        
    return selected

def check_answer(user_input, correct_answer):
    if not user_input:
        return False
    clean_user = str(user_input).strip().lower()
    clean_correct = str(correct_answer).strip().lower()
    
    if clean_user == clean_correct:
        return True
        
    try:
        if float(clean_user) == float(clean_correct):
            return True
    except ValueError:
        pass
        
    return False
