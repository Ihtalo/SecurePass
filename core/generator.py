import random

WORDS = [
    "Sun", "Moon", "River", "Tiger", "Cloud",
    "Sky", "Fire", "Ocean", "Stone", "Wind"
]

SYMBOLS = "!@#$%&*"

def generate_password():
    word1 = random.choice(WORDS)
    word2 = random.choice(WORDS)
    number = str(random.randint(10, 99))
    symbol = random.choice(SYMBOLS)

    return f"{word1}{symbol}{number}{word2}"