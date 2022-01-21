import random

GREY = 0
YELLOW = 1
GREEN = 2

ANSI_RED = "\u001B[31m"
ANSI_GREEN = "\u001B[32m"
ANSI_YELLOW = "\u001B[33m"
ANSI_RESET = "\u001B[0m"


def load_words():
    with open('resources/5_letter_words.txt') as word_file:
        words = word_file.read().split()
    return words


all_words = load_words()


def random_word():
    return random.choice(all_words)
