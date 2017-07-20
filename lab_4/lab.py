"""6.009 Lab 4 -- HyperMines"""


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
             "state: {}".format(game["state"])]
    print("\n".join(lines))


def nd_get(nd_array, coords, n):
    """Get element at coords in nd_array.

    Arguments:
        nd_array (list): N-dimensional input array
        coords (tuple): Coordinates of interest
        n (int) : tracks number of recursions

    Returns:
        An array element

    >>> nd_get([[[0, 1], [2, 3]], [[4, 5], [5, 6]]], (0, 1, 1), 0)
    3
    """

    if n == len(coords) - 1:
        return nd_array[coords[n]]
    return nd_get(nd_array[coords[n]], coords, n + 1)


def nd_set(nd_array, coords, value):
    """Set element at coords in nd_array.

    Arguments:
        nd_array (list): N-dimensional input array
        coords (tuple): Coordinates of interest
        value: Value to put at coords

    >>> elements = [[[3, '.'], [3, 3], [1, 1], [0, 0]],[['.', 3], [3, '.'], [1, 1], [0, 0]]]
    >>> nd_set(elements, (0, 1, 1), '.')
    >>> print(elements)
    [[[3, '.'], [3, '.'], [1, 1], [0, 0]], [['.', 3], [3, '.'], [1, 1], [0, 0]]]
    """

    coords = list(coords)
    for x in coords[:-1]:
        nd_array = nd_array[x]
    nd_array[coords[-1]] = value


def nd_product(sequence):
    """Produce the Cartesian product of sequences.

    Arguments:
        sequence (list): Sequences to compute the product of

    Returns:
        A list of tuples
    //>>> for n in nd_product([(1, 2, 3), ("a", "b")]): print(n)
    >>> list(nd_product([(1, 2, 3), ("a", "b")]))
    (1, 'a')
    (1, 'b')
    (2, 'a')
    (2, 'b')
    (3, 'a')
    (3, 'b')
    """

    if not sequence:
        return iter(((),))
    return (items + (item,)
            for items in nd_product(sequence[:-1]) for item in sequence[-1])


def nd_neighbors(game, coords):
    """Produce all neighbors of coords in game.

    Arguments:
        game (dict): Game state
        coords (tuple): Reference point

    Returns:
        An iterable of coordinates

    >>> game = {"dimensions": [2, 4, 2],
    ... "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ... [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ... "mask": [[[False, False], [False, True], [False, False], [False, False]],
    ... [[False, False], [False, False], [False, False], [False, False]]]}
    >>> sorted(nd_neighbors(game, (1, 2, 0)))
    [(0, 1, 0), (0, 1, 1),
    (0, 2, 0), (0, 2, 1),
    (0, 3, 0), (0, 3, 1),
    (1, 1, 0), (1, 1, 1),
    (1, 2, 0), (1, 2, 1),
    (1, 3, 0), (1, 3, 1)]
    """
    list = []
    for n in range(len(coords)):
        t = ()
        for i in range(coords[n]-1, coords[n]+2):
            if 0 <= i < game["dimensions"][n]:
                t = t + (i,)
        list.append(t)
    return nd_product(list)


def nd_mkboard(dims, filler, n):
    """Create a board with dimensions dims, and fill it with filler.

    Arguments:
        dims (list): List of board dimensions
        filler (Any): Value to initialize the board with
        n (int): tracks recursion

    Returns:
        A len(dims)-dimensional array
        >>> n = nd_mkboard([2, 3, 2], 42, 0)
        >>> print(n)
        [[[42, 42], [42, 42], [42, 42]], [[42, 42], [42, 42], [42, 42]]]
        >>> nd_set(n, (0,0,1), '.')
        >>> print(n)
        [[[42, '.'], [42, 42], [42, 42]], [[42, 42], [42, 42], [42, 42]]]
    """
    if n == len(dims):
        return filler
    return [nd_mkboard(dims, filler, n + 1) for x in range(dims[n])]


def nd_game_status(game):
    """Compute game status.

    Return one of "ongoing", "victory", or "defeat".
    >>> game = {"dimensions": [2, 4, 2],
    ...         "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                   [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...         "mask": [[[True, False], [True, True], [True, True], [True, True]],
    ...                  [[False, True], [True, False], [True, True], [True, True]]],
    ...         "state": "ongoing"}
    >>> nd_game_status(game)
    'victory'
    """
    coords = nd_coords(game)
    covered = 0
    for c in coords:
        revealed = nd_get(game["mask"], c, 0)
        item = nd_get(game["board"], c, 0)
        if item == '.' and revealed is True:
            return "defeat"
        if item != '.' and revealed is False:
            covered += 1
    if covered > 0:
        return "ongoing"
    return "victory"


def nd_new_game(dims, bombs):
    """Start a new game.

    Return a game state dictionary, with the "board" and "mask" fields
    adequately initialized.  This is an N-dimensional version of new_game().

    Args:
       dims (list): Dimensions of the board
       bombs (list): Bomb locations as a list of lists, each an N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> dump(nd_new_game([2, 4, 2], [[0, 0, 1], [1, 0, 0], [1, 1, 1]]))
    dimensions: [2, 4, 2]
    board: [[3, '.'], [3, 3], [1, 1], [0, 0]]
           [['.', 3], [3, '.'], [1, 1], [0, 0]]
    mask:  [[False, False], [False, False], [False, False], [False, False]]
           [[False, False], [False, False], [False, False], [False, False]]
    state: ongoing
    """

    # fills boards
    b = nd_mkboard(dims, 0, 0)
    m = nd_mkboard(dims, False, 0)

    for coords in bombs:
        nd_set(b, coords, '.')
        neighbors = nd_neighbors({"dimensions": dims, "board" : b, "mask" : m, "state": "ongoing"}, coords)
        for n in neighbors:
            item = nd_get(b, n, 0)
            if item != '.':
                nd_set(b, n, item + 1)

    return {"dimensions": dims, "board" : b, "mask" : m, "state": "ongoing"}


def nd_dig(game, coords):
    """Recursively dig up square at coords and neighboring squares.

    Update game["mask"] to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    bomb.  Return a number indicating how many squares were revealed.  No action
    should be taken and 0 returned if the incoming state of the game is not "ongoing".

    The updated state is "defeat" when at least one bomb is visible on the board
    after digging (i.e. game["mask"][bomb_location] == True), "victory" when all
    safe squares (squares that do not contain a bomb) and no bombs are visible,
    and "ongoing" otherwise.

    This is an N-dimensional version of dig().

    Args:
       game (dict): Game state
       coords (list): Where to start digging

    Returns:
       int: number of squares revealed

    >>> game = {"dimensions": [2, 4, 2],
    ...         "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                   [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...         "mask": [[[False, False], [False, True], [False, False], [False, False]],
    ...                  [[False, False], [False, False], [False, False], [False, False]]],
    ...         "state": "ongoing"}
    >>> nd_dig(game, [0, 3, 0])
    8
    >>> dump(game)
    dimensions: [2, 4, 2]
    board: [[3, '.'], [3, 3], [1, 1], [0, 0]]
           [['.', 3], [3, '.'], [1, 1], [0, 0]]
    mask:  [[False, False], [False, True], [True, True], [True, True]]
           [[False, False], [False, False], [True, True], [True, True]]
    state: ongoing
    >>> game = {"dimensions": [2, 4, 2],
    ...         "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                   [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...         "mask": [[[False, False], [False, True], [False, False], [False, False]],
    ...                  [[False, False], [False, False], [False, False], [False, False]]],
    ...         "state": "ongoing"}
    >>> nd_dig(game, [0, 0, 1])
    1
    >>> dump(game)
    dimensions: [2, 4, 2]
    board: [[3, '.'], [3, 3], [1, 1], [0, 0]]
           [['.', 3], [3, '.'], [1, 1], [0, 0]]
    mask:  [[False, True], [False, True], [False, False], [False, False]]
           [[False, False], [False, False], [False, False], [False, False]]
    state: defeat
    """
    coords = tuple(coords)

    if game["state"] == "defeat" or game["state"] == "victory":
        return 0

    if nd_get(game["mask"], coords, 0):
        return 0

    if nd_get(game["board"], coords, 0) == '.':
        nd_set(game["mask"], coords, True)
        game["state"] = "defeat"
        return 1

    revealed = reveal_squares(game, coords)
    game["state"] = nd_game_status(game)
    return revealed


def reveal_squares(game, coords):
    """Helper function: recursively reveal squares on the board, and return
    the number of squares that were revealed.

    Args:
       game (dict): Game state
       coords (tuple): Where to reveal

    Returns:
        int: number of squares revealed
    >>> game = {"dimensions": [2, 4, 2],
    ...         "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                   [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...         "mask": [[[False, False], [False, True], [False, False], [False, False]],
    ...                  [[False, False], [False, False], [False, False], [False, False]]],
    ...         "state": "ongoing"}
    >>> reveal_squares(game, (0, 0, 1))
    1
    """

    if nd_get(game["board"], coords, 0) != 0:
        if nd_get(game["mask"], coords, 0):
            return 0
        else:
            nd_set(game["mask"], coords, True)
            return 1
    else:
        revealed = set()
        neighbors = nd_neighbors(game, coords)
        for n in neighbors:
            if nd_get(game["board"], n, 0) != '.' and not nd_get(game["mask"], n, 0):
                nd_set(game["mask"], n, True)
                revealed.add(n)
        total = len(revealed)
        for r in revealed:
            if nd_get(game["board"], r, 0) != ".":
                total += reveal_squares(game, r)
        return total


def nd_coords(game):
    """Helper function: creates a list containing every possible coordinate.

        Args:
           game (dict): Game state

        Returns:
            list: tuple coordinates
    >>> game = {"dimensions": [2, 2, 2],
    ...         "board": [[[3, '.'], [3, 3]],
    ...                   [['.', 3], [3, '.']]],
    ...         "mask": [[[False, False], [False, True]],
    ...                  [[False, False], [False, False]]],
    ...         "state": "ongoing"}
    >>> for n in nd_coords(game): print(n)
    (0, 0, 0)
    (0, 0, 1)
    (0, 1, 0)
    (0, 1, 1)
    (1, 0, 0)
    (1, 0, 1)
    (1, 1, 0)
    (1, 1, 1)
    """
    coords = []
    for i in game["dimensions"]:
        t = ()
        for j in range(i):
            t = t + (j,)
        coords.append(t)
    return nd_product(coords)


def nd_render(game, xray=False):
    """Prepare a game for display.

    Returns an N-dimensional array (nested lists) of "_" (hidden squares), "."
    (bombs), " " (empty squares), or "1", "2", etc. (squares neighboring bombs).
    game["mask"] indicates which squares should be visible.  If xray is True (the
    default is False), game["mask"] is ignored and all cells are shown.

    This is an N-dimensional version of render().

    Args:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game["mask"]

    Returns:
       An n-dimensional array (nested lists)

    >>> nd_render({"dimensions": [2, 4, 2],
    ...            "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                      [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...            "mask": [[[False, False], [False, True], [True, True], [True, True]],
    ...                     [[False, False], [False, False], [True, True], [True, True]]],
    ...            "state": "ongoing"},
    ...           False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']], [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> nd_render({"dimensions": [2, 4, 2],
    ...            "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                      [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...            "mask": [[[False, False], [False, True], [False, False], [False, False]],
    ...                     [[False, False], [False, False], [False, False], [False, False]]],
    ...            "state": "ongoing"},
    ...           True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']], [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """

    coords = nd_coords(game)

    masked = nd_mkboard(game["dimensions"], '-1', 0)
    for c in coords:
        if not xray and not nd_get(game["mask"], c, 0):
            nd_set(masked, c, '_')
        elif nd_get(game["board"], c, 0) == 0:
            nd_set(masked, c, ' ')
        else:
            nd_set(masked, c, str(nd_get(game["board"], c, 0)))
    return masked
