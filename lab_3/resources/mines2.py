# rows are copies of themselves
# new game doesn't have a game state - can't be used
# is victory doesn't check if covered squares left

def neighbors(dimensions, r, c):
    all_neighbors = [(r+i, c+j) for i in range(-1,2) for j in range(-1, 2)]
    return [(x,y) for (x,y) in all_neighbors if 0 <= x < dimensions[0] and 0 <= y < dimensions[1]]


# rows are copies of themselves
def make_board(nrows, ncols, elem):
    row = [elem]*ncols
    return [row]*nrows


def new_game(num_rows, num_cols, bombs):
    mask = make_board(num_rows, num_cols, False)
    board = make_board(num_rows, num_cols, 0) 
    for br, bc in bombs:
        board[br][bc] = '.'
    for br, bc in bombs:
        for nr, nc in neighbors([num_rows, num_cols], br, bc):
            if board[nr][nc] != '.':
                board[nr][nc] += 1
    # no state present
    return {"dimensions": [num_cols, num_rows], "board" : board, "mask" : mask}


def reveal_squares_2d(game, row, col):
    if game["board"][row][col] != 0:
        if game["mask"][row][col]:
            return 0
        game["mask"][row][col] = True
        return 1

    revealed = set()
    for r, c in neighbors(game["dimensions"], row, col):
        if game["board"][r][c] != '.' and not game["mask"][r][c]:
            game["mask"][r][c] = True
            revealed.add((r, c))

    total = len(revealed)
    for r,c in revealed:
        if game["board"][r][c] != "." :
            total += reveal_squares_2d(game, r, c)
    return total

# doesn't check if there are covered squares left
def is_victory(game):
    for r in range(game["dimensions"][0]):
        for c in range(game["dimensions"][1]):
            if game["board"][r][c] == '.' and game["mask"][r][c]:
                return False
    return True


def dig(game, row, col):
    if game["board"][row][col] == '.':
        game["mask"][row][col] = True
        game["state"] = 'defeat'
        return 1

    if is_victory(game):
        game['state'] = 'victory'
        return 0
    
    revealed = reveal_squares_2d(game, row, col)
    status = 'victory' if is_victory(game) else 'ongoing' 
    game["state"] = status
    return revealed


def render(game, xray=False):
    nrows, ncols = game['dimensions']
    board = game['board']
    return [['_' if (not xray) and (not game['mask'][r][c]) else
             ' ' if board[r][c] == 0 else str(board[r][c])
             for c in range(ncols)] for r in range(nrows)]


def render_ascii(game, xray=False):
    return "\n".join((("%s"*len(r)) % tuple(r)) for r in render(game, xray=xray))
