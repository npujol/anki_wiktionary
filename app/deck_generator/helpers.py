import random


def generate_random_id() -> int:
    """Generates a random 10-digit ID."""
    return random.randint(a=1000000000, b=9999999999)
