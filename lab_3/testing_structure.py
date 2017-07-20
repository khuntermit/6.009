# this file structures each test as a single function that returns True if the
# module correctly implemented that behavior, and False otherwise.

# make sure you understand how the test_mines_implementation function at the
# bottom of this file is put together and how it makes use of these testing
# functions.

def test_newgame_dimensions(mines_imp):
    pass # your code here


def test_newgame_board(mines_imp):
    pass # your code here


def test_newgame_mask(mines_imp):
    pass # your code here


def test_newgame_state(mines_imp):
    pass # your code here


def test_dig_mask(mines_imp):
    pass # your code here


def test_dig_reveal(mines_imp):
    pass # your code here


def test_dig_neighbors(mines_imp):
    pass # your code here


def test_completed_dig_nop(mines_imp):
    pass # your code here


def test_multiple_dig_nop(mines_imp):
    pass # your code here


def test_dig_count(mines_imp):
    pass # your code here


def test_defeat_state(mines_imp):
    pass # your code here


def test_victory_state(mines_imp):
    pass # your code here


all_tests = {
    'newgame_dimensions': test_newgame_dimensions,
    'newgame_board': test_newgame_board,
    'newgame_mask': test_newgame_mask,
    'newgame_state': test_newgame_state,
    'dig_mask': test_dig_mask,
    'dig_reveal': test_dig_reveal,
    'dig_neighbors': test_dig_neighbors,
    'completed_dig_nop': test_completed_dig_nop,
    'multiple_dig_nop': test_multiple_dig_nop,
    'dig_count': test_dig_count,
    'defeat_state': test_defeat_state,
    'victory_state': test_victory_state,
}

success_names = {False: 'incorrect', True: 'correct'}

def test_mines_implementation(mines_imp):
    out = {i: [] for i in success_names.values()}
    incorrect = []
    for name, func in all_tests.items():
        try:
            success = func(mines_imp)
        except:
            success = False
        out[success_names[success]].append(name)
    return out
