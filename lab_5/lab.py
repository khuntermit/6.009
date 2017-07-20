# NO IMPORTS!


# returns a list of occupied squares for an anchor and shape
def squares(anchor, shape):
    """Converts an anchor and a shape to the squares occupied.

    Arguments:
        anchor (tuple): Anchor
        shape (set): Set of tuple coords

    Returns:
        A list of newly occupied squares


    >>> squares((1, 1), {(0, 0), (1, 0), (2, 0)})
    {(3, 1), (1, 1), (2, 1)}
    """
    ans = []
    for s in shape:
        ans.append((s[0] + anchor[0], s[1] + anchor[1]))
    return set(ans)


# returns a set of all squares occupied by bags on the board
def occupied(board, bag_list):
    """Calculates all occupied squares on the board

    Arguments:
        board (list): List of dictionaries representing people
        bag_list (list): List of sets representing bag shapes

    Returns:
        A set of all squares occupied on the board


    >>> occupied([{"anchor":(0, 0), "shape":0}], [{(0, 0), (1, 0), (2, 0)}])
    {(2, 0), (1, 0), (0, 0)}
    """
    filled = []
    for b in board:
        anchor = b["anchor"]
        shape = bag_list[b["shape"]]
        filled += squares(anchor, shape)
    return set(filled)


# finds the next empty square to fill
def next_cell(tent_size, missing_squares, board, bag_list):
    """Returns the tuple coordinate of the next cell to fill

    Arguments:
        tent_size (tuple): Tent size
        missing_squares (set): Set of rock locations
        board (list): List of dictionaries representing people
        bag_list (list): List of sets representing bag shapes

    Returns:
        A tuple coordinate of the next open cell, (-1, -1) if none exists.


    >>> next_cell((5, 5), {(0, 0), (0, 1), (0, 2)}, [], [{(0, 0), (1, 0), (2, 0)}])
    (0, 3)
    >>> next_cell((2, 1), {(0, 0), (1, 0)}, [], [{(0, 0), (1, 0), (2, 0)}])
    (-1, -1)
    """
    for x in range(0, tent_size[0]):
        for y in range(0, tent_size[1]):
            if (x, y) not in occupied(board, bag_list) and (x, y) not in missing_squares:
                return x, y
    return -1, -1


# checks if bag placement is valid
def is_valid(tent_size, missing_squares, bag_list, board, bag):
    """Returns True if the placement is valid, otherwise returns False

    For each square (r,c) occupied by a sleeping bag 0 <= r < nrows and 0 <= c < ncols
    (i.e. each person lies entirely within the tent).
    No rock exists under (r,c) (i.e. no person sleeps on a rock).
    No two people have a square in common (i.e. no two people overlap).

    Arguments:
        tent_size (tuple): Tent size
        missing_squares (set): Set of rock locations
        board (list): List of dictionaries representing people
        bag_list (list): List of sets representing bag shapes
        bag (dictionary): Describes a bag with "anchor" and "shape"

    Returns:
        True if placement is valid, False otherwise.

    >>> is_valid((4, 4), {(0, 0), (0, 1)}, [{(0, 0), (1, 0), (2, 0)}], [], {"anchor": (1, 0), "shape": 0})
    True
    >>> is_valid((4, 4), {(0, 0), (0, 1)}, [{(0, 0), (1, 0), (2, 0)}], [], {"anchor": (0, 0), "shape": 0})
    False
    """
    filled = occupied(board, bag_list)
    new_squares = squares(bag["anchor"], bag_list[bag["shape"]])
    for n in new_squares:
        # checks that each new square fills an unoccupied spot
        if n in filled or n in missing_squares:
            return False
        # checks if each new square is within the boundary
        if not 0 <= n[0] < tent_size[0] or not 0 <= n[1] < tent_size[1]:
            return False
    return True


# Pack a tent with different sleeping bag shapes leaving no empty squares
#
# INPUTS:
#   tent_size = (rows,cols) for tent grid
#   missing_squares = set of (r,c) tuples giving location of rocks
#   bag_list = list of sets, each decribing a sleeping bag shape
#      Each set contains (r,c) tuples enumerating contiguous grid
#      squares occupied by bag, coords are relative to the upper-
#      left corner of bag.  You can assume every bag occupies
#      at least the grid (0,0).
#
# Example bag_list entries:
#      vertical 3x1 bag: { (0,0), (1,0), (2,0) }
#      horizontal 1x3 bag: { (0,0), (0,1), (0,2) }
#      square bag: { (0,0), (0,1), (1,0), (1,1) }
#      L-shaped bag: { (0,0), (1,0), (1,1) }
#      C-shaped bag: { (0,0), (0,1), (1,0), (2,0), (2,1) }
#      reverse-C-shaped bag: { (0,0), (0,1), (1,1), (2,0), (2,1) }
#
# OUTPUT:
#   None if no packing can be found
#   a list giving the placement and type for each placed bag
#   expressed as a dictionary with keys
#     "anchor": (r,c) for upper-left corner of bag
#     "shape": index of bag on bag list


def pack(tent_size, missing_squares, bag_list):
    board = []
    result = solve(tent_size, missing_squares, bag_list, board)
    if result:
        return board
    return None


backtracks = 0


def solve(tent_size, missing_squares, bag_list, board, i=0, j=0):
    """ Recursively finds the best packing and returns a list of placements or returns None

    Arguments:
        tent_size (tuple): Tent size
        missing_squares (set): Set of rock locations
        bag_list (list): List of sets representing bag shapes
        board (list): List of dictionaries representing people

    Returns:
        board (list): List of dictionaries representing people
    """
    global backtracks

    if backtracks > (tent_size[0] * tent_size[1] * len(bag_list)):
        return False

    # Find the next cell to fill
    i, j = next_cell(tent_size, missing_squares, board, bag_list)
    if i == -1:
        return True

    for shape in range(len(bag_list)):
        # Try different shapes in i, j location

        bag = {"anchor": (i, j), "shape": shape}
        if is_valid(tent_size, missing_squares, bag_list, board, bag):

            board.append({"anchor": (i, j), "shape": shape})

            if solve(tent_size, missing_squares, bag_list, board, i, j):
                return True

    backtracks += 1
    # Undo the current cell for backtracking
    if len(board) > 0:
        board.pop()

    return False
