# wordle solver
#
# basic idea is to compare known possible letters and position against a list of (almost) all 5 letter words and pick a
# word that matches the criteria and eliminates about half of the remaining choices.
# First start off with some random word with preferably no repeats. The most common letters are E, T, A, R, I, O,
# N, and S. So something like train, ratio, or arise might be good starts. We can also use ouija to knock out the most
# common vowels.

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
DEBUG = True


def load_words():
    with open('resources/5_letter_words.txt') as word_file:
        words = word_file.read().split()
    return words


def check_word(word, exclude, include, exclude_positions, letter_positions):
    word_set = set(word)

    for letter in word_set:
        if letter in exclude:
            return False
    for letter in include:
        if letter not in word_set:
            return False
    for i in exclude_positions:
        for letter in exclude_positions[i]:
            if letter == word[i]:
                return False
    for i in letter_positions:
        if letter_positions[i] != word[i]:
            return False
    return True


def filter_words(words, exclude, exclude_positions, letter_positions):
    include = set(letter for letters in exclude_positions.values() for letter in letters)

    filtered = []
    for word in words:
        if check_word(word, exclude, include, exclude_positions, letter_positions):
            filtered.append(word)
    return filtered


# based on the remaining possible letters (not in exclude, technically letters in the letter positions can be repeated)
# choose a word that splits the remaining list in half (choose letters that only half of the words have)
def next_guess(words, exclude):
    possible_letters = set([letter for letter in ALPHABET if letter not in exclude])
    frequencies = {}

    for word in words:
        for letter in set(word):
            if letter in possible_letters:
                if letter not in frequencies:
                    frequencies[letter] = 0
                frequencies[letter] += 1

    distances = {}
    for letter in possible_letters:
        if letter not in frequencies:
            continue
        distances[letter] = abs(.5 - frequencies[letter] / len(words))

    if len(distances) == 0:
        print('no possible words')
        return
    best_letter = min(distances, key=distances.get)

    if DEBUG:
        print(f'best letter is guess is {best_letter} with a score of {1 - distances[best_letter]:.3f}')
        print(f'{len(words)} remaining possible word(s)')
        if len(words) < 11:
            print(f'{words}')

    possible_words = []
    for word in words:
        if best_letter in set(word):  # try to find a word with no repeats too
            possible_words.append(word)
        if len(possible_words) > 5:
            return possible_words
    return possible_words


def solve(words, exclude, exclude_positions, letter_positions):
    words = filter_words(words, exclude, exclude_positions, letter_positions)
    return next_guess(words, exclude)


def main():
    words = load_words()
    exclude = set()
    exclude_positions = {}
    letter_positions = {}

    while True:
        if len(exclude) != 0:
            print(f'excluded: {exclude}')
        # print('Enter letters to exclude (grey letters):')
        exclude.update(set(input('Enter letters to exclude (grey letters):')))

        if len(exclude_positions) != 0:
            print(f'included: {exclude_positions}')
        # print('Enter positions of (yellow) letters to include (use ? for unknowns):')
        yellow = input('Enter positions of (yellow) letters to include (use ? for unknowns):')

        for i in range(len(yellow)):
            if yellow[i] in ALPHABET:
                if i not in exclude_positions:
                    exclude_positions[i] = set()
                exclude_positions[i].add(yellow[i])

        if len(letter_positions) != 0:  # maybe rename to green positions
            print(f'current positions: {letter_positions}')
        # print('Enter positions of known (green) letters (use ? for unknowns):')
        green = input('Enter positions of known (green) letters (use ? for unknowns):')

        #  add not position. or maybe have them enter in the guess?
        for i in range(len(green)):
            if green[i] in ALPHABET:
                letter_positions[i] = green[i]

        guess = solve(words, exclude, exclude_positions, letter_positions)

        print(f'Try {guess}.')
        input("Press Enter to continue...")


if __name__ == '__main__':
    main()
    print('done')


