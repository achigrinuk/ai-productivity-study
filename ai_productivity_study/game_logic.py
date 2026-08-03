import random
from typing import Dict, Tuple, Any


class PuzzleGenerator:
    """Generates diverse puzzle types for the productivity study."""

    def __init__(self):
        self.puzzle_types = ['arithmetic', 'word_scramble', 'pattern', 'logic']
        self.words = [
            'PYTHON', 'STREAMLIT', 'RESEARCH', 'SCIENCE', 'BEHAVIOR',
            'EXPERIMENT', 'DATA', 'ANALYSIS', 'COGNITIVE', 'DECISION',
            'PRODUCTIVITY', 'ASSISTANCE', 'METHODOLOGY', 'STATISTICS',
            'HYPOTHESIS', 'VARIABLE', 'CORRELATION', 'SIGNIFICANCE', 'SAMPLE',
            'CONDITIONAL', 'ALGORITHM', 'COMPUTATION', 'VALIDATION', 'LOGIC',
            'PATTERN', 'SEQUENCE', 'MATRIX', 'PROBABILITY', 'INFERENCE'
        ]

    def generate_puzzle(self, puzzle_type=None) -> Dict[str, Any]:
        if puzzle_type is None:
            puzzle_type = random.choice(self.puzzle_types)

        generator_method = getattr(self, f'_generate_{puzzle_type}', self._generate_arithmetic)
        return generator_method()

    def _generate_arithmetic(self) -> Dict[str, Any]:
        """Generate an arithmetic problem."""
        operations = ['+', '-', '*', '/']
        op = random.choice(operations)

        if op == '+':
            a, b = random.randint(1, 50), random.randint(1, 50)
            question = f"What is {a} + {b}?"
            answer = a + b
        elif op == '-':
            a, b = random.randint(10, 100), random.randint(1, 10)
            question = f"What is {a} - {b}?"
            answer = a - b
        elif op == '*':
            a, b = random.randint(1, 12), random.randint(1, 12)
            question = f"What is {a} x {b}?"
            answer = a * b
        else:  # division
            b = random.randint(1, 10)
            a = b * random.randint(1, 10)
            question = f"What is {a} / {b}?"
            answer = a // b

        return {
            'type': 'arithmetic',
            'question': question,
            'solution': str(answer)
        }

    def _generate_word_scramble(self) -> Dict[str, Any]:
        """Generate a word scramble puzzle."""
        word = random.choice(self.words)
        letters = list(word)
        scrambled = None
        while True:
            random.shuffle(letters)
            scrambled = ''.join(letters)
            if scrambled != word:
                break

        return {
            'type': 'word_scramble',
            'question': f"Unscramble the letters to form a word: {scrambled}",
            'solution': word.lower()
        }

    def _generate_pattern(self) -> Dict[str, Any]:
        """Generate a pattern recognition puzzle."""
        pattern_types = ['arithmetic_seq', 'geometric_seq', 'alternating']
        ptype = random.choice(pattern_types)

        if ptype == 'arithmetic_seq':
            start = random.randint(1, 10)
            diff = random.randint(2, 5)
            seq = [start + i * diff for i in range(5)]
            question = f"What number comes next in this sequence: {', '.join(map(str, seq[:4]))}?"
            answer = seq[4]

        elif ptype == 'geometric_seq':
            start = random.randint(1, 10)
            ratio = random.choice([2, 3, 4])
            seq = [start * (ratio ** i) for i in range(5)]
            if all(s < 100 for s in seq):
                question = f"What number comes next in this sequence: {', '.join(map(str, seq[:4]))}?"
                answer = seq[4]
            else:
                question = f"What number comes next in this sequence: {', '.join(map(str, seq[:4]))}?"
                answer = seq[4]

        else:  # alternating
            pairs = [(random.randint(10, 50), random.randint(2, 8)) for _ in range(2)]
            seq = [pairs[0][0], pairs[0][0] + pairs[1][1], pairs[0][0] + pairs[1][1] + pairs[0][1]]
            question = f"What number comes next in this sequence: {seq[0]}, {seq[1]}?"
            answer = seq[2]

        return {
            'type': 'pattern',
            'question': question,
            'solution': str(answer)
        }

    def _generate_logic(self) -> Dict[str, Any]:
        """Generate a logic puzzle."""
        logic_puzzles = [
            {
                'question': "If all Bloops are Razzies and all Razzies are Loppies, then all Bloops are definitely Loppies. Is this true or false?",
                'solution': 'true'
            },
            {
                'question': "If a plane crashes on the border of USA and Canada, where do survivors go?",
                'solution': 'survivors do not need to go anywhere'
            },
            {
                'question': "A doctor and a father are in a car accident. The father dies, but the child survives. The child is taken to the hospital, and the surgeon says, 'I can't operate on this boy, he is my son.' How is this possible?",
                'solution': "the surgeon is the child's mother"
            },
            {
                'question': "What gets wetter as it dries?",
                'solution': 'towel'
            },
            {
                'question': "How many months have 28 days?",
                'solution': 'all of them'
            }
        ]

        puzzle = random.choice(logic_puzzles)

        return {
            'type': 'logic',
            'question': puzzle['question'],
            'solution': puzzle['solution']
        }


class AIAssistant:
    """Provides AI assistance in the form of hints or answers."""

    def __init__(self):
        self.hints = [
            "Let's break this down step by step.",
            "Consider the fundamental operations involved.",
            "Think about what the question is really asking.",
            "You can use the elimination method to narrow down options.",
            "Focus on the key numbers or terms in the problem.",
            "Remember to check your work after calculating.",
        ]

    def provide_hint(self, puzzle: Dict[str, Any], hint_level: int = 1) -> str:
        """Provide a hint based on the puzzle type."""
        ptype = puzzle['type']

        if ptype == 'arithmetic':
            if hint_level == 1:
                return "Identify the operation needed to solve this problem (addition, subtraction, multiplication, or division)."
            else:
                return f"The operation is: {puzzle['question'].split()[2] if '+' in puzzle['question'] else 'apply the correct operation'}."
        elif ptype == 'word_scramble':
            if hint_level == 1:
                return "Look at the scrambled letters and try to form recognizable prefixes or suffixes."
            else:
                first_letter = puzzle['solution'][0] if puzzle['solution'] else '?'
                return f"The word starts with the letter '{first_letter.upper()}'."
        elif ptype == 'pattern':
            if hint_level == 1:
                return "Analyze the relationship between consecutive numbers to find the pattern."
            else:
                return "Consider whether the pattern involves addition, multiplication, or alternating rules."
        elif ptype == 'logic':
            if hint_level == 1:
                return "Read the question carefully - sometimes the answer is hidden in the wording."
            else:
                return "Try to think of the problem from a different perspective."

        return random.choice(self.hints)

    def provide_answer(self, puzzle: Dict[str, Any]) -> str:
        """Provide the correct answer."""
        return puzzle['solution']


def validate_answer(puzzle: Dict[str, Any], user_answer: str) -> bool:
    """Validate the user's answer against the puzzle solution."""
    correct = puzzle['solution']
    user = user_answer.strip().lower()

    if puzzle['type'] == 'arithmetic':
        try:
            return abs(int(user) - int(correct)) < 0.01
        except ValueError:
            return False
    elif puzzle['type'] == 'word_scramble':
        return user == correct.lower()
    elif puzzle['type'] == 'pattern':
        try:
            return abs(int(user) - int(correct)) < 0.01
        except ValueError:
            return False
    elif puzzle['type'] == 'logic':
        user = user.replace(' ', '').lower()
        correct_clean = correct.replace(' ', '').lower()
        return user == correct_clean or correct_clean in user

    return user == correct.lower()


def run_trial(puzzle: Dict[str, Any], user_answer: str) -> Tuple[bool, str]:
    """Run a single trial and return (is_correct, correct_solution)."""
    is_correct = validate_answer(puzzle, user_answer)
    return is_correct, puzzle['solution']
