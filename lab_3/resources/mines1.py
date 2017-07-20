# is victory doesn't work right
# return true in loop
# dig status var unused
# mix up r and c

def neighbors(dimensions, r, c):
    all_neighbors = [(r+i, c+j) for i in range(-1,2) for j in range(-1, 2)]
    return [(x,y) for (x,y) in all_neighbors if 0 <= x < dimensions[0] and 0 <= y < dimensions[1]]


def new_game(num_rows, num_cols, bombs):
    """Start a new game."""
    mask = [[False]*num_cols for r in range(num_rows)]
    board = [[0]*num_cols for r in range(num_rows)]
    for bx, by in bombs:
        board[by][bx] = '.'
    for x in range(num_rows):
        for y in range(num_cols):
            if board[y][x] == 0:
                for nx, ny in neighbors([num_rows, num_cols], x, y):
                    if board[ny][nx] == '.':
                        board[y][x] += 1
    return {"dimensions": [num_rows, num_cols], "board" : board, "mask" : mask, "state": "ongoing"}

def num_covered(game):
    total = 0
    for r in range(game["dimensions"][0]):
        for c in range(game["dimensions"][1]):
            if not game["mask"][r][c]:
                total += 1
    return total

def reveal_squares_2d(game, row, col):
    initial_covered = num_covered(game)
    # never changes mask state
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

    for r,c in revealed:
        if game["board"][r][c] != "." :
            reveal_squares_2d(game, r, c)
    return initial_covered - num_covered(game)


# doesn't check for covered squares
def is_victory(game):
    for r in range(game["dimensions"][0]):
        for c in range(game["dimensions"][1]):
            if game["board"][r][c] == '.' and game["mask"][r][c]:
                return False
            else:
                return True
    return True

# sets status
def dig(game, row, col):
    if game["board"][row][col] == '.':
        game["mask"][row][col] = True
        game["state"] = 'defeat'
        return 1
    
    if is_victory(game):
        game['state'] = 'victory'
        return 0
    
    revealed = reveal_squares_2d(game, row, col)
    # sets status but doesn't assign that to game state
    status = 'victory' if is_victory(game) else 'ongoing' 
    game["state"] = "ongoing"
    return revealed


def render(game, xray=False):
    nrows, ncols = game['dimensions']
    board = game['board']
    return [['_' if (not xray) and (not game['mask'][r][c]) else
             ' ' if board[r][c] == 0 else str(board[r][c])
             for c in range(ncols)] for r in range(nrows)]


def render_ascii(game, xray=False):
    return "\n".join((("%s"*len(r)) % tuple(r)) for r in render(game, xray=xray))
