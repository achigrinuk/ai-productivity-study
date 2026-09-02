import random

RAW_PUZZLE_BANK = [
    # Tier 1: Factual / Algorithmic (Direct Math & Patterns)
    {
        "id": "seq_2_4_8",
        "question": "What comes next in the sequence: 2, 4, 8, 16, ___?",
        "answer": "32",
        "hint_accurate": "Each number doubles the previous number.",
        "hint_flawed": "Add 6 to the previous number (16 + 6).",
        "type": "Algorithmic",
        "complexity": "Tier 1"
    },
    {
        "id": "math_15_12",
        "question": "What is 15 x 12?",
        "answer": "180",
        "hint_accurate": "15 x 10 = 150, then add 15 x 2.",
        "hint_flawed": "Multiply 15 x 10 = 150, then add 12 = 162.",
        "type": "Algorithmic",
        "complexity": "Tier 1"
    },
    {
        "id": "math_144_12",
        "question": "What is 144 / 12?",
        "answer": "12",
        "hint_accurate": "12 squared equals 144.",
        "hint_flawed": "Divide 144 by 10, then subtract 2.",
        "type": "Algorithmic",
        "complexity": "Tier 1"
    },
    {
        "id": "seq_3_6_12",
        "question": "What comes next in the sequence: 3, 6, 12, 24, ___?",
        "answer": "48",
        "hint_accurate": "Multiply by 2 each step.",
        "hint_flawed": "Add 12 to the previous number.",
        "type": "Algorithmic",
        "complexity": "Tier 1"
    },

    # Tier 2: Cognitive Reflection / Intuitive Tricks
    {
        "id": "logic_bat_ball",
        "question": "A bat and ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much is the ball in cents?",
        "answer": "5",
        "hint_accurate": "Let ball = x. Then x + (x + 1.00) = 1.10, so 2x = 0.10.",
        "hint_flawed": "Since total is $1.10 and bat is $1.00, the ball costs 10 cents.",
        "type": "Cognitive Reflection",
        "complexity": "Tier 2"
    },
    {
        "id": "logic_lily_pads",
        "question": "In a lake, there is a patch of lily pads. Every day, the patch doubles in size. If it takes 48 days to cover the lake, how many days to cover half?",
        "answer": "47",
        "hint_accurate": "If it doubles every day, it was half full the day before day 48.",
        "hint_flawed": "To cover half the lake, divide total days by 2 (48 / 2 = 24 days).",
        "type": "Cognitive Reflection",
        "complexity": "Tier 2"
    },
    {
        "id": "logic_machines",
        "question": "If 5 machines take 5 minutes to make 5 widgets, how many minutes would 100 machines take to make 100 widgets?",
        "answer": "5",
        "hint_accurate": "1 machine takes 5 minutes to make 1 widget.",
        "hint_flawed": "100 machines making 100 widgets scales linearly, taking 100 minutes.",
        "type": "Cognitive Reflection",
        "complexity": "Tier 2"
    },

    # Tier 3: Word Scrambles & Verbal Logic
    {
        "id": "scramble_coding",
        "question_type": "scramble",
        "word": "coding",
        "hint_accurate": "It's what software engineers do.",
        "hint_flawed": "An activity done with paper and pencil.",
        "type": "Verbal Logic",
        "complexity": "Tier 3"
    },
    {
        "id": "scramble_python",
        "question_type": "scramble",
        "word": "python",
        "hint_accurate": "A popular programming language named after a snake.",
        "hint_flawed": "A ancient Greek city state.",
        "type": "Verbal Logic",
        "complexity": "Tier 3"
    },
    {
        "id": "scramble_algorithm",
        "question_type": "scramble",
        "word": "algorithm",
        "hint_accurate": "A step-by-step procedure for solving a problem.",
        "hint_flawed": "A musical composition technique.",
        "type": "Verbal Logic",
        "complexity": "Tier 3"
    }
]

def scramble_word(word):
    chars = list(word.upper())
    while True:
        random.shuffle(chars)
        scrambled = " ".join(chars)
        if scrambled != " ".join(list(word.upper())):
            return scrambled

def generate_puzzle(exclude_list=None):
    if exclude_list is None:
        exclude_list = []
        
    available = [p for p in RAW_PUZZLE_BANK if p['id'] not in exclude_list]
    if not available:
        available = RAW_PUZZLE_BANK
        
    selected = random.choice(available).copy()
    
    # 25% Chance to deliver a Flawed/Hallucinated AI Hint
    is_hallucinated = random.random() < 0.25
    selected['is_hallucinated'] = is_hallucinated
    selected['selected_hint'] = selected['hint_flawed'] if is_hallucinated else selected['hint_accurate']
    
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
