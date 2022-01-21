import util

GREY = 0
YELLOW = 1
GREEN = 2

ANSI_RED = "\u001B[31m"
ANSI_GREEN = "\u001B[32m"
ANSI_YELLOW = "\u001B[33m"
ANSI_RESET = "\u001B[0m"


def check_guess(answer, guess):
    result = []
    for i in range(len(guess)):
        if guess[i] not in answer:
            result.append(GREY)
        elif guess[i] == answer[i]:
            result.append(GREEN)
        else:
            result.append(YELLOW)
    return result


def print_guess(result, guess):
    for i in range(len(guess)):
        color_type = ANSI_RED
        if result[i] == YELLOW:
            color_type = ANSI_YELLOW
        elif result[i] == GREEN:
            color_type = ANSI_GREEN
        print(f'{color_type}{guess[i]}{ANSI_RESET}', end='')
    print()


def play_round(guess, answer):
    result = check_guess(answer, guess)
    print_guess(result, guess)
    if sum(result) == len(answer) * GREEN:
        return False
    return True


def game(answer=util.random_word()):
    num_guesses = 0
    retry = True
    while retry:
        guess = input('Enter guess:')
        retry = play_round(guess, answer)
        num_guesses += 1
    print(f'You won in {num_guesses} guesses!')
    return num_guesses


def main():
    exclude = set()
    include = set()
    correct = set()

    answer = util.random_word()
    answer = 'train'
    guesses = game(answer)


if __name__ == '__main__':
    main()
    print('done')
