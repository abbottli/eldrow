import math
import eldrow
import util
import multiprocessing as mp
from timeit import default_timer as timer

DEBUG = False


def check_guess(answer, guess):
    result = []
    for i in range(len(guess)):
        if guess[i] not in answer:
            result.append(util.GREY)
        elif guess[i] == answer[i]:
            result.append(util.GREEN)
        else:
            result.append(util.YELLOW)
    return result


def check(answer, guess, exclude, exclude_positions, letter_positions):
    if DEBUG:
        print(f'guessing {guess}')
    result = check_guess(answer, guess)
    if sum(result) == len(answer) * util.GREEN:
        return False
    for i in range(len(guess)):
        if result[i] == util.GREY:
            exclude.add(guess[i])
        elif result[i] == util.YELLOW:
            if i not in exclude_positions:
                exclude_positions[i] = []
            exclude_positions[i].append(guess[i])
        else:
            if i not in letter_positions:
                letter_positions[i] = []
            letter_positions[i] = guess[i]
    return True


def game(answer=util.random_word(), guess=util.random_word()):
    exclude = set()
    exclude_positions = {}
    letter_positions = {}
    words = util.all_words
    num_guesses = 1

    retry = check(answer, guess, exclude, exclude_positions, letter_positions)

    while retry:
        guess = eldrow.solve(words, exclude, exclude_positions, letter_positions)[0]
        retry = check(answer, guess, exclude, exclude_positions, letter_positions)
        num_guesses += 1
    if DEBUG:
        print(f'You won in {num_guesses} guesses! answer: {answer}')
    return num_guesses


def sim_all(first_guess):
    results = {}
    for answer in util.all_words:
        guesses = game(answer, first_guess)
        results[answer] = guesses
    return results


def sim_range(first_guess, i, amount, q):
    results = {}
    offset = i * amount
    for i in range(amount):
        if i % 50 == 0:
            print('.', end='', flush=True)
        if offset + i == len(util.all_words):
            break
        answer = util.all_words[offset + i]
        guesses = game(answer, first_guess)
        results[answer] = guesses
    q.put(results)


def progress_listener(q):
    results = {}
    while True:
        response = q.get()
        if response == 'kill':
            q.put(results)
            break
        results.update(response)
        if DEBUG:
            print(f'got response {response}')


def main():
    process_count = mp.cpu_count()
    manager = mp.Manager()
    q = manager.Queue()
    pool = mp.Pool(process_count)

    listener = pool.apply_async(progress_listener, [q])

    results = {}
    # first_guess = 'train'
    words_to_test = ['train', 'arise', 'ratio', 'ouija']

    for first_guess in words_to_test:
        jobs = []
        start = timer()
        words_per_process = math.ceil(len(util.all_words) / process_count)
        for i in range(process_count):
            job = pool.apply_async(sim_range, (first_guess, i, words_per_process, q))
            jobs.append(job)

        for job in jobs:
            job.get()

        q.put('kill')
        results[first_guess] = q.get()
        end = timer()
        print(f'\ncalculated {len(util.all_words)} words in {end - start:.2f}s for guess {first_guess}')

    listener.get()
    pool.close()
    pool.join()

    print('Finished processing. Calculating stats')

    stats = {}
    for guess in results:
        avg = sum(results[guess].values()) / len(results[guess].values())
        max_word = max(results[guess], key=results[guess].get)

        stats[guess] = {
            'avg': f'{avg:.3f}',
            'max': max_word,
            'max_count': results[guess][max_word]
        }
    print(stats)


if __name__ == '__main__':
    main()
    print('done')
