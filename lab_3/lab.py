"""6.009 Lab 3 -- Six Double-Oh Mines"""


def dump(game):
    """Print a human-readable representation of game.

    Arguments:
       game (dict): Game state


    >>> dump({'dimensions': [1, 2], 'mask': [[False, False]], 'board': [['.', 1]], 'state': 'ongoing'})
    dimensions: [1, 2]
    board: ['.', 1]
    mask:  [False, False]
    state: ongoing
    """
    lines = ["dimensions: {}".format(game["dimensions"]),
             "board: {}".format("\n       ".join(map(str, game["board"]))),
             "mask:  {}".format("\n       ".join(map(str, game["mask"]))),
             "state: {}".format(game["state"]),
             ]
    print("\n".join(lines))


def neighbors(num_rows, num_cols, r, c):
    all_neighbors = [(r+i, c+j) for i in range(-1,2) for j in range(-1, 2)]
    return [(x,y) for (x,y) in all_neighbors if 0 <= x < num_rows and 0 <= y < num_cols]


def new_game(num_rows, num_cols, bombs):
    """Start a new game.

    Return a game state dictionary, with the "state", "board" and "mask" fields
    adequately initialized.

    Args:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs

    Returns:
       A game state dictionary

    >>> dump(new_game(2, 4, [(0, 0), (1, 0), (1, 1)]))
    dimensions: [2, 4]
    board: ['.', 3, 1, 0]
           ['.', '.', 1, 0]
    mask:  [False, False, False, False]
           [False, False, False, False]
    state: ongoing
    """
    # help document suggested a separate function
    # helper functions define how each board should be filled
    def board_fill(r, c, bombs):
        if (r, c) in bombs:
            return '.'
        return 0

    def mask_fill(r, c, bombs):
        return False

    # fills boards
    board = populate_arrays(num_rows, num_cols, bombs, board_fill)
    mask = populate_arrays(num_rows, num_cols, bombs, mask_fill)

    # made a looping structure to replace redundancy
    for r in range(num_rows):
        for c in range(num_cols):
            if board[r][c] == 0:
                neighbor_bombs = 0
                # made a function to find the surrounding squares
                around = neighbors(num_rows, num_cols, r, c)
                for a in around:
                    if a in bombs:
                        neighbor_bombs += 1
                board[r][c] = neighbor_bombs
    return {"dimensions": [num_rows, num_cols], "board": board, "mask": mask, "state": "ongoing"}


# helper function to fill the boards
def populate_arrays(num_rows, num_cols, bombs, f):
    board = []
    for r in range(num_rows):
        row = []
        for c in range(num_cols):
            row.append(f(r, c, bombs))
        board.append(row)
    return board


def reveal_squares(game, row, col):
    """Helper function: recursively reveal squares on the board, and return
    the number of squares that were revealed."""
    board = game["board"]
    mask = game["mask"]
    x = game["dimensions"][0]
    y = game["dimensions"][1]

    if board[row][col] != 0:
        if mask[row][col]:
            return 0
        else:
            mask[row][col] = True
            return 1
    else:
        revealed = set()
        around = neighbors(x, y, row, col)
        # removed for loop and replaced with a function call
        for a in around:
            r = a[0]
            c = a[1]
            if board[r][c] != '.' and not mask[r][c]:
                mask[r][c] = True
                revealed.add((r, c))
        total = len(revealed)
        for r, c in revealed:
            if board[r][c] != ".":
                total += reveal_squares(game, r, c)
        return total


def dig(game, row, col):
    """Recursively dig up (row, col) and neighboring squares.

    Update game["mask"] to reveal (row, col); then recursively reveal (dig up)
    its neighbors, as long as (row, col) does not contain and is not adjacent
    to a bomb.  Return an integer indicating how many new squares were
    revealed.

    The state of the game should be changed to "defeat" when at least one bomb
    is visible on the board after digging (i.e. game["mask"][bomb_location] ==
    True), "victory" when all safe squares (squares that do not contain a bomb)
    and no bombs are visible, and "ongoing" otherwise.

    Args:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {"dimensions": [2, 4],
    ...         "board": [[".", 3, 1, 0],
    ...                   [".", ".", 1, 0]],
    ...         "mask": [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         "state": "ongoing"}
    >>> dig(game, 0, 3)
    4
    >>> dump(game)
    dimensions: [2, 4]
    board: ['.', 3, 1, 0]
           ['.', '.', 1, 0]
    mask:  [False, True, True, True]
           [False, False, True, True]
    state: victory

    >>> game = {"dimensions": [2, 4],
    ...         "board": [[".", 3, 1, 0],
    ...                   [".", ".", 1, 0]],
    ...         "mask": [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         "state": "ongoing"}
    >>> dig(game, 0, 0)
    1
    >>> dump(game)
    dimensions: [2, 4]
    board: ['.', 3, 1, 0]
           ['.', '.', 1, 0]
    mask:  [True, True, False, False]
           [False, False, False, False]
    state: defeat
    """

    state = game["state"]
    if state == "defeat" or state == "victory":
        game["state"] = state
        return 0

    # left as is
    if game["board"][row][col] == '.':
        game["mask"][row][col] = True
        game["state"] = "defeat"
        return 1

    # removed entire second block - redundant

    revealed = reveal_squares(game, row, col)
    # combined covered_squares and bombs into bad_squares
    bad_squares = 0
    for r in range(game["dimensions"][0]):
        for c in range(game["dimensions"][1]):
            if game["board"][r][c] is ".":
                if game["mask"][r][c]:
                    bad_squares += 1
            elif not game["mask"][r][c]:
                bad_squares += 1
    if bad_squares == 0:
        game["state"] = "victory"
    return revealed


def render(game, xray=False):
    """Prepare a game for display.

    Returns a two-dimensional array (list of lists) of "_" (hidden squares), "."
    (bombs), " " (empty squares), or "1", "2", etc. (squares neighboring bombs).
    game["mask"] indicates which squares should be visible.  If xray is True (the
    default is False), game["mask"] is ignored and all cells are shown.

    Args:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game["mask"]

    Returns:
       A 2D array (list of lists)

    >>> render({"dimensions": [2, 4],
    ...         "board": [[".", 3, 1, 0],
    ...                   [".", ".", 1, 0]],
    ...         "mask":  [[False, True, True, False],
    ...                   [False, False, True, False]]}, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render({"dimensions": [2, 4],
    ...         "board": [[".", 3, 1, 0],
    ...                   [".", ".", 1, 0]],
    ...         "mask":  [[False, True, False, True],
    ...                   [False, False, False, True]]}, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """

    # makes board for viewing
    masked_board = []
    x_range = game["dimensions"][0]
    y_range = game["dimensions"][1]
    for x in range(x_range):
        row = []
        for y in range(y_range):
            # if xray is off and cell is masked
            if not xray and not game["mask"][x][y]:
                row.append("_")
            # if entry is 0 at that coord
            elif game["board"][x][y] == 0:
                row.append(" ")
            # converts all entries to strings
            else:
                row.append(str(game["board"][x][y]))
        masked_board.append(row)

    return masked_board


def render_ascii(game, xray=False):
    """Render a game as ASCII art.

    Returns a string-based representation of argument "game".  Each tile of the
    game board should be rendered as in the function "render(game)".

    Args:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game["mask"]

    Returns:
       A string-based representation of game

    >>> print(render_ascii({"dimensions": [2, 4],
    ...                     "board": [[".", 3, 1, 0],
    ...                               [".", ".", 1, 0]],
    ...                     "mask":  [[True, True, True, False],
    ...                               [False, False, True, False]]}))
    .31_
    __1_
    """
    x_range = game["dimensions"][0]
    y_range = game["dimensions"][1]
    rendering = render(game, xray)
    ascii = ""
    for x in range(x_range):
        # adds paragraphs
        if x > 0:
            ascii = ascii + "\n"
        # adds characters from render to String
        for y in range(y_range):
            ascii = ascii + rendering[x][y]
    return ascii


# test cases


# the dimensions should be initialized correctly
def test_newgame_dimensions(mines_imp):
    game = mines_imp.new_game(2, 4, [(0, 0), (1, 0), (1, 1)])
    # checks dimensions
    return game["dimensions"][0] is 2 and game["dimensions"][1] is 4


# the board should be initialized correctly
def test_newgame_board(mines_imp):
    game = mines_imp.new_game(2, 4, [(0, 0), (1, 0), (1, 1)])
    board = game["board"]
    # checks board against correct board
    return board == [['.', 3, 1, 0], ['.', '.', 1, 0]]


# the mask should be initialized correctly
def test_newgame_mask(mines_imp):
    game = mines_imp.new_game(2, 4, [(0, 0), (1, 0), (1, 1)])
    mask = [[False, False, False, False], [False, False, False, False]]

    # checks against the implementation of bad array duplication
    game["mask"][0][0] = True
    if game["mask"][1][0]:
        return False
    game["mask"][0][0] = False
    return game["mask"] == mask


# the game state should be initialized correctly
def test_newgame_state(mines_imp):
    game = mines_imp.new_game(2, 4, [(0, 0), (1, 0), (1, 1)])
    # checks if initial state is ongoing
    return game["state"] is "ongoing"


# digging should modify the mask, not the game board
def test_dig_mask(mines_imp):
    game = new_game(5, 5, [(0, 2), (0, 3), (0, 4)])
    game2 = new_game(5, 5, [(0, 2), (0, 3), (0, 4)])
    # board and render before
    before_board = game2["board"]
    before = render(game, False)
    # dig three times
    mines_imp.dig(game, 1, 2)
    mines_imp.dig(game, 1, 3)
    mines_imp.dig(game, 1, 4)
    # board and render after
    after = render(game, False)
    # boards should be equal and renders should be different
    return before_board == game["board"] and before != after


# digging should reveal the square that was dug
def test_dig_reveal(mines_imp):
    game = new_game(3, 4, [(0, 0), (1, 0), (1, 1), (2, 2)])
    mines_imp.dig(game, 0, 2)
    # checks the render to see if value is showing
    rend = render(game, False)
    return rend[0][2] == "1"


# all neighbors of a 0 should be dug
def test_dig_neighbors(mines_imp):
    game = new_game(5, 5, [(0, 0), (0, 4), (4, 0), (4, 4)])
    # stores initial board
    final_board = game["board"]

    mines_imp.dig(game, 2, 2)
    rend = mines_imp.render(game, False)
    dug = False
    # checks if rendering surrounding bombs shows 1s
    if rend[0][1] and rend[4][1] and rend[4][3] and rend[0][3] == "1":
        dug = True
    # return if the boards match and the digging works
    return game["board"] == final_board and dug


# dig should not do anything on a game that is not ongoing
def test_completed_dig_nop(mines_imp):
    game = mines_imp.new_game(1, 3, [(0, 2)])
    before = render(game, False)
    # change state to victory and dig
    game["state"] = "victory"
    mines_imp.dig(game, 0, 0)
    # change state to defeat and dig
    game["state"] = "defeat"
    mines_imp.dig(game, 0, 0)
    # render should not change
    after = render(game, False)
    return before == after


# dig should not do anything on a square that was already dug
def test_multiple_dig_nop(mines_imp):
    game = new_game(5, 5, [(0, 0), (3, 4), (2, 2)])
    mines_imp.dig(game, 0, 2)
    # stores surrounding bombs
    cell_num = mines_imp.dig(game, 0, 2)
    # cell number and state should remain the same
    return cell_num == 0 and (game["state"] == "ongoing")


# digging should correctly report all of the tiles that were dug
def test_dig_count(mines_imp):
    # makes a new game, mask should start as all False
    game = new_game(1, 3, [(0, 2)])
    # stores number dug
    dug = mines_imp.dig(game, 0, 0)
    # finds the correct number dug (counts all Trues)
    correct_num = 0
    for x in range(0, 1):
        for y in range(0, 3):
            if game["mask"][x][y]:
                correct_num += 1
    return dug == correct_num


# digging a mine should result in the defeat state
def test_defeat_state(mines_imp):
    game = new_game(2, 4, [(0, 0), (1, 0), (1, 1)])
    # digs a mine
    mines_imp.dig(game, 1, 1)
    return game["state"] is "defeat"


# game state should change to victory when there are no safe squares
def test_victory_state(mines_imp):
    game = new_game(1, 5, [(0, 1), (0, 4)])

    # digs and runs tests against each state
    mines_imp.dig(game, 0, 0)
    test1 = game["state"] == "ongoing"
    mines_imp.dig(game, 0, 3)
    test2 = game["state"] == "ongoing"
    mines_imp.dig(game, 0, 2)
    test3 = game["state"] == "victory"

    return test1 and test2 and test3


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
    """Test whether an implementation of the mines game correctly implements
    all the desired behaviors.

    Returns a dictionary with two keys: 'correct' and 'incorrect'.  'correct'
    maps to a list containing the string names of the behaviors that were
    implemented correctly (as given in the readme); and 'incorrect' maps to a
    list containing the string descriptions of the behaviors that were
    implemented incorrectly.

    Args:
        mines_imp: a module containing implementations of the new_game, dig,
                   and render functions.

                   for example, the dig function can be accessed with:
                       mines_imp.dig(game, row, col)

    Returns:
       A dictionary mapping strings to sequences.
    """

    out = {i: [] for i in success_names.values()}
    incorrect = []
    for name, func in all_tests.items():
        try:
            success = func(mines_imp)
        except:
            success = False
        out[success_names[success]].append(name)
    return out


if __name__ == "__main__":
    import doctest

    doctest.testmod()
