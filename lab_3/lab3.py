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
    board = []
    for r in range(num_rows):
        row = []
        for c in range(num_cols):
            if [r,c] in bombs or (r,c) in bombs:
                row.append('.')
            else:
                row.append(0)
        board.append(row)
    mask = []
    for r in range(num_rows):
        row = []
        for c in range(num_cols):
            row.append(False)
        mask.append(row)
    for r in range(num_rows):
        for c in range(num_cols):
            if board[r][c] == 0:
                neighbor_bombs = 0
                if 0 <= r-1 < num_rows:
                    if 0 <= c-1 < num_cols:
                        if board[r-1][c-1] == '.':
                            neighbor_bombs += 1
                if 0 <= r < num_rows:
                    if 0 <= c-1 < num_cols:
                        if board[r][c-1] == '.':
                            neighbor_bombs += 1
                if 0 <= r+1 < num_rows:
                    if 0 <= c-1 < num_cols:
                        if board[r+1][c-1] == '.':
                            neighbor_bombs += 1
                if 0 <= r-1 < num_rows:
                    if 0 <= c < num_cols:
                        if board[r-1][c] == '.':
                            neighbor_bombs += 1
                if 0 <= r < num_rows:
                    if 0 <= c < num_cols:
                        if board[r][c] == '.':
                            neighbor_bombs += 1
                if 0 <= r+1 < num_rows:
                    if 0 <= c < num_cols:
                        if board[r+1][c] == '.':
                            neighbor_bombs += 1
                if 0 <= r-1 < num_rows:
                    if 0 <= c+1 < num_cols:
                        if board[r-1][c+1] == '.':
                            neighbor_bombs += 1
                if 0 <= r < num_rows:
                    if 0 <= c+1 < num_cols:
                        if board[r][c+1] == '.':
                            neighbor_bombs += 1
                if 0 <= r+1 < num_rows:
                    if 0 <= c+1 < num_cols:
                        if board[r+1][c+1] == '.':
                            neighbor_bombs += 1
                board[r][c] = neighbor_bombs
    return {"dimensions": [num_rows, num_cols], "board" : board, "mask" : mask, "state": "ongoing"}


def reveal_squares(game, row, col):
    """Helper function: recursively reveal squares on the board, and return
    the number of squares that were revealed."""
    if game["board"][row][col] != 0:
        if game["mask"][row][col]:
            return 0
        else:
            game["mask"][row][col] = True
            return 1
    else:
        revealed = set()
        for r in range(row - 1, row + 2):
            if r < game["dimensions"][0]:
                if r >= 0:
                    for c in range(col - 1, col + 2):
                        if c < game["dimensions"][1]:
                            if c >= 0:
                                if game["board"][r][c] != '.' and not game["mask"][r][c] == True:
                                    game["mask"][r][c] = True
                                    revealed.add((r, c))
        total = len(revealed)
        for r,c in revealed:
            if game["board"][r][c] != "." :
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

    if game["board"][row][col] == '.':
        game["mask"][row][col] = True
        game["state"] = "defeat"
        return 1
    
    bombs = 0
    covered_squares = 0
    for r in range(game["dimensions"][0]):
        for c in range(game["dimensions"][1]):
            if game["board"][r][c] == ".":
                if  game["mask"][r][c] == True:
                    bombs += 1
            elif game["mask"][r][c] == False:
                covered_squares += 1
    if bombs != 0:
        game["state"] = "defeat"
        return 0
    if covered_squares == 0:
        game["state"] = "victory"
        return 0
    
    revealed = reveal_squares(game, row, col)
    bombs = 0
    covered_squares = 0
    for r in range(game["dimensions"][0]):
        for c in range(game["dimensions"][1]):
            if game["board"][r][c] == ".":
                if  game["mask"][r][c] == True:
                    bombs += 1
            elif game["mask"][r][c] == False:
                covered_squares += 1
    bad_squares = bombs + covered_squares
    if bad_squares > 0:
        game["state"] = "ongoing"
        return revealed
    else:
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
    masked_board = game["board"][:]
    x_range = game["dimensions"][0]
    y_range = game["dimensions"][1]
    for x in range(x_range):
        for y in range(y_range):
            # if entry is 0 at that coord
            if masked_board[x][y] is 0:
                # turn it into a space
                masked_board[x][y] = " "
            # converts all entries to strings
            convert = str(game["board"][x][y])
            masked_board[x][y] = convert
            # if the xray is off
            if not xray:
                # mask whichever coord is False
                if not game["mask"][x][y]:
                    masked_board[x][y] = "_"
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
    raise NotImplementedError


if __name__ == "__main__":
    import doctest
    doctest.testmod()
