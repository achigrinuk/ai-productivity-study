import random

RAW_PUZZLE_BANK = [
    {"question_type": "scramble", "word": "coding", "hint": "It's what software engineers do.", "type": "scramble"},
    {"question_type": "scramble", "word": "python", "hint": "A popular programming language named after a snake.", "type": "scramble"},
    {"question_type": "scramble", "word": "algorithm", "hint": "A set of rules to solve a problem in computer science.", "type": "scramble"},
    {"question": "What comes next in the sequence: 2, 4, 8, 16, ___?", "answer": "32", "hint": "Each number doubles the previous number.", "type": "pattern"},
    {"question": "If 5 workers build 5 tables in 5 hours, how many hours does 1 worker take to build 1 table?", "answer": "5", "hint": "Think about individual worker rate.", "type": "logic"},
    {"question": "What is 15 x 12?", "answer": "180", "hint": "15 x 10 = 150, then add 15 x 2.", "type": "math"},
    {"question": "What comes next in the sequence: 3, 6, 12, 24, ___?", "answer": "48", "hint": "Multiply by 2 each step.", "type": "pattern"},
    {"question": "Which is heavier: a pound of feathers or a pound of bricks?", "answer": "neither", "hint": "Pay close attention to the units of weight.", "type": "logic"},
    {"question": "What is 144 / 12?", "answer": "12", "hint": "12 squared equals 144.", "type": "math"},
    {"question": "What comes next: 1, 1, 2, 3, 5, 8, ___?", "answer": "13", "hint": "Add the two previous numbers (Fibonacci sequence).", "type": "pattern"},
    {"question": "A bat and ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much is the ball in cents?", "answer": "5", "hint": "Let ball = x, bat = x + 1.00. 2x + 1.00 = 1.10.", "type": "logic"},
    {"question": "What is 25 x 4 - 15?", "answer": "85", "hint": "Multiply 25 by 4 first, then subtract 15.", "type": "math"}
]

def scramble_word(word):
    """Takes a word and randomly shuffles its letters."""
    chars = list(word.upper())
    # Shuffle until the scrambled version is different from the original word
    while True:
        random.shuffle(chars)
        scrambled = " ".join(chars)
        if scrambled != " ".join(list(word.upper())):
            return scrambled

def generate_puzzle(exclude_list=None):
    if exclude_list is None:
        exclude_list = []
        
    available = [p for p in RAW_PUZZLE_BANK if p.get('question', p.get('word')) not in exclude_list]
    if not available:
        available = RAW_PUZZLE_BANK
        
    selected = random.choice(available).copy()
    
    # If it's a scramble question, dynamically scramble the letters
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
    
    # Check exact match
    if clean_user == clean_correct:
        return True
        
    # Handle simple numeric edge cases (e.g. 5 vs 5.0)
    try:
        if float(clean_user) == float(clean_correct):
            return True
    except ValueError:
        pass
        
    return False
