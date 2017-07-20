# 6.009 Quiz 1 Practice 1, Spring 2017

# NOTE: NO IMPORTS ALLOWED!

##################################################
##  Problem 1. hangman
##################################################

# Please implement the function hangman(secret_word,guessed_letters)
# where both secret_word and guessed_letters are lists of characters.
# hangman should return a list of characters showing the secret word
# with unguessed characters displayed as underscores.

def hangman(secret_word, guessed_letters):
    """
    `hangman(['h','i'],[])` should return `['_','_']`.

    `hangman(['b','o','o','k','k','e','e','p','e','r'],['o','e'])` should return `['_','o','o','_','_','e','e','_','e','_']`.

    `hangman(['q','u','i','n','q','u','u','x'],['i','u','q','n','x'])` should return `['q','u','i','n','q','u','u','x']`.

    """
    for let in range(len(secret_word)):
        if secret_word[let] not in guessed_letters:
            secret_word[let] = '_'
    return secret_word




##################################################
##  Problem 2. mode
##################################################

# Given a list of numbers, return the mode or the mean of modes if
# there are more than one mode. The mode is a number that appears
# most often in the list. It does not have to be unique, since
# several different numbers may appear the same number of times.
# In those cases, you need to return the mean of the modes.

def mode(numbers):
    """
    `mode([314159, 314159, 2048, 333])` should return `314159`.

    `mode([1, 1, 2, 2, 3])` should return `1.5`.
    """
    occ = {}
    for num in numbers:
        if num not in occ:
            occ[num] = 1
        else:
            occ[num] += 1
    max = 0
    for num, occurences in occ.items():
        if occurences > max:
            max = occurences
    mode = []
    for num, occurences in occ.items():
        if occurences == max:
            mode.append(num)
    if len(mode) == 1:
        return mode[0]
    else:
        answer = 0
        for i in mode:
            answer+=i
        answer = answer/len(mode)
        return answer


##################################################
##  Problem 3. most_repeated_character
##################################################

# Given a list of characters, find sequences of a single repeated
# character.  Return the length of the longest such sequence or 0
# if there are no sequences of a single repeated character.  Note
# that there may be several longest sequences.

def most_repeated_character(characters):
    """
    `most_repeated_character([])` should return `0`.

    `most_repeated_character(['a','b','c','a','b','c'])` should return `1`.

    `most_repeated_character(['a','b','c','a','a','a'])` should return `3`.

    `most_repeated_character(['a','a','b','b','c','c'])` should return `2`.
    """
    max_repeats = 0
    repeats = 1
    for i in range(len(characters)):
        if i > 0:
            if characters[i] == characters[i-1]:
                repeats += 1
            else:
                repeats = 1
        if repeats > max_repeats:
            max_repeats = repeats
    return max_repeats




##################################################
##  Problem 4. integer_right_triangles
##################################################

# Let p be the perimeter of a right triangle with integral, non-zero
# length sides of length a, b, and c. Implement the function
# integer_right_triangles(p) which returns a sorted list of
# solutions with perimeter p.

def integer_right_triangles(p):
    """
    `integer_right_triangles(12)` returns `[[3,4,5]]`

    `integer_right_triangles(60)` returns `[[10,24,26], [15,20,25]]`

    `integer_right_triangles(152)` returns `[]`
    """
    def is_right_tri(a, b, c):
        side_a = a ** 2
        side_b = b ** 2
        side_c = c ** 2
        if side_a + side_b == side_c:
            return True
        return False

    def perim(a, b, c, p):
        if a + b + c == p:
            return True
        return False

    def rec_tri(solutions, a, b, c, p):
        if is_right_tri(a, b, c) and perim(a, b, c, p):
            sol = [a, b, c]
            if sol not in solutions:
                solutions.append(sol)

    solutions = []
    for a in range(1, int(p / 2)):
        for b in range(a, int((p - a + 2) / 2)):
                rec_tri(solutions, a, b, p - a - b, p)

    return solutions

####################################################
##  Problem 5. Encoding Nested Lists
####################################################

def encode(seq):
    """Encode a sequence of nested lists as a flat list.

    Arguments:
       seq (list): A sequence of nested lists of integers.

    Returns:
       list: A flat sequence of integers, 'up's, and 'down's.
          Each 'up' indicates an increase in the nesting level;
          each 'down' indicates a decrease in the nesting level.

    Note:
       You can use isinstance(x, list) to check whether x is a list:
          >>> isinstance([1, 2], list), isinstance(1, list)
          (True, False)

    >>> encode([])
    ['up', 'down']

    >>> encode([1])
    ['up', 1, 'down']

    >>> encode([1, [2], 1])
    ['up', 1, 'up', 2, 'down', 1, 'down']

    >>> encode([[[1, [2]]]])
    ['up', 'up', 'up', 1, 'up', 2, 'down', 'down', 'down', 'down']

    >>> encode([[1, 2, 3], [[[1]]], 6, [2, 3, [12, 9, 8, 6], 47], [1, []]])
    ['up', 'up', 1, 2, 3, 'down', 'up', 'up', 'up', 1, 'down',
     'down', 'down', 6, 'up', 2, 3, 'up', 12, 9, 8, 6, 'down',
     47, 'down', 'up', 1, 'up', 'down', 'down', 'down']

    Note: please do not use 'eval' or 'exec'.
    Examples:

    Note: We recommend using Python's built-in function `isinstance(x, list)` to check whether `x` is a list, in cases where `x` might also be a number.
    """
    # def val(seq, final):
    #     for i in range(len(seq)):
    #         if not isinstance(seq[i], list):
    #             return seq[i]
    #         if len(seq[i]) == 1:
    #
    #             return val(i)
    return []



