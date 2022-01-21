# eldrow
A basic wordle solver.

## Usage
Run `eldrow.py` and follow the prompts.
1. Enter in the letters that aren't in the word (grey letters)
2. Enter in the letters that aren't positioned correctly (yellow letters)
    * use a non-alphabet character like `?` to represent unknowns/blanks
3. Enter in the letters that are positioned correctly (green letters)

eldrow will then give you some possible word options to choose from.

Example game starting with `arise`
```
Enter letters to exclude (grey letters):rise
Enter positions of (yellow) letters to include (use ? for unknowns):a????
Enter positions of known (green) letters (use ? for unknowns):
Try ['badly', 'baldy', 'balky', 'bally', 'balmy', 'banal'].
Press Enter to continue...

excluded: {'r', 's', 'i', 'e'}
Enter letters to exclude (grey letters):bdy
included: {0: {'a'}}
Enter positions of (yellow) letters to include (use ? for unknowns):?a?l?
Enter positions of known (green) letters (use ? for unknowns):
Try ['cloak', 'float', 'focal', 'gloat', 'loath', 'local'].
Press Enter to continue...

excluded: {'y', 'd', 's', 'b', 'r', 'i', 'e'}
Enter letters to exclude (grey letters):ft
included: {0: {'a'}, 1: {'a'}, 3: {'l'}}
Enter positions of (yellow) letters to include (use ? for unknowns):?lo??
Enter positions of known (green) letters (use ? for unknowns):???a?
Try ['local', 'vocal'].
(local was the answer)
```

## How it works
Under the hood, eldrow will filter a list of 5 letter words based on the initial requirements. It'll then make a
 frequency map of the letters to figure out which one splits the remaining words in have (or as close to half as possible)
 to reduce the number of remaining choices.

## Starting words
You can start with whatever word you want and eldrow will still be able to find the word in time.
Obviously some initial starts are better than others. A word that contain the most common letters,
for example, will be able to narrow down the list of possible answers faster than other words. 

Some possible starts: `train`, `ratio`, `arise`, `ouija` 

## Debug mode
In the files themselves, the `DEBUG` flag can be turned on for additional info about some of the internal metrics
e.g. same game as above with `DEBUG` on
```
Enter letters to exclude (grey letters):rise
Enter positions of (yellow) letters to include (use ? for unknowns):a????
Enter positions of known (green) letters (use ? for unknowns):
best letter is guess is l with a score of 0.833
291 remaining possible word(s)
Try ['badly', 'baldy', 'balky', 'bally', 'balmy', 'banal'].
Press Enter to continue...

excluded: {'s', 'e', 'i', 'r'}
Enter letters to exclude (grey letters):bdy
included: {0: {'a'}}
Enter positions of (yellow) letters to include (use ? for unknowns):?a?l?
Enter positions of known (green) letters (use ? for unknowns):
best letter is guess is o with a score of 0.984
31 remaining possible word(s)
Try ['cloak', 'float', 'focal', 'gloat', 'loath', 'local'].
Press Enter to continue...

excluded: {'s', 'b', 'e', 'd', 'r', 'y', 'i'}
Enter letters to exclude (grey letters):ft
included: {0: {'a'}, 1: {'a'}, 3: {'l'}}
Enter positions of (yellow) letters to include (use ? for unknowns):?lo??
Enter positions of known (green) letters (use ? for unknowns):???a?
best letter is guess is c with a score of 1.000
4 remaining possible word(s)
['local', 'molal', 'vocal', 'zonal']
Try ['local', 'vocal'].
Press Enter to continue...
```

## game.py
A sample wordle game is provided via `game.py` if you want to play it but the real version is way better

## sim.py
`sim.py` runs simulated games against the `eldrow.py` logic and outputs performance stats at the end. It takes around 15s
to go through all 5757 words for a given guess.
Example output
```python
{'train': {'avg': '4.439', 'max': 'sills', 'max_count': 11},
 'arise': {'avg': '3.678', 'max': 'bears', 'max_count': 11}, # so fast :)
 'ratio': {'avg': '4.122', 'max': 'cases', 'max_count': 10},
 'ouija': {'avg': '4.511', 'max': 'gales', 'max_count': 11}}
```

Ideally, I'd run this sim on all 5757 words to figure out what's the best/worst, but at its current state, that would take
two months to run :o

