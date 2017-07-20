# doesn't iterate correctly in new game
# game can't end in defeat - breaks when bomb is clicked bc state is kept ongoing
# cannot click on the square to reveal if it is not a blank or a bomb bc doesn't handle numbers in dig

def neighbors(dimensions, r, c):
    all_neighbors = [(r+i, c+j) for i in range(-1,2) for j in range(-1, 2)]
    return [(x,y) for (x,y) in all_neighbors if 0 <= x < dimensions[0] and 0 <= y < dimensions[1]]


def make_board(nrows, ncols, elem):
    return [[elem for c in range(ncols)] for r in range(nrows)]


def new_game(num_rows, num_cols, bombs):
    mask = make_board(num_rows, num_cols, False)

    board = make_board(num_rows, num_cols, 0)
    # not the correct way to iterate through bombs
    for br, bc in bombs:
        board[br][bc] = '.'
    for br, bc in bombs:
        for nr, nc in neighbors([num_rows, num_cols], br, bc):
            if board[nr][nc] != '.':
                board[nr][nc] = 1
    return {"dimensions": [num_rows, num_cols], "board" : board, "mask" : mask, "state": "ongoing"}


# does not reach victory when all safe squares are cleared
def is_victory(game):
    for r in range(game["dimensions"][0]):
        for c in range(game["dimensions"][1]):
            # uncovered bomb
            if game["board"][r][c] == '.' and game["mask"]:
                return False
            # if the mask is False at that square
            elif not game['mask'][r][c]:
                return False
    return True


def dig(game, row, col):
    if is_victory(game):
        game['state'] = 'victory'
        return 0

    # where does dig handle numbers?

    # bomb
    if game["board"][row][col] == '.':
        game["mask"][row][col] = True
        # state is kept ongoing
        game['state'] = 'ongoing'
        return 1

    # zero
    count = 1
    if game['board'][row][col] == 0:
        for nr, nc in neighbors(game['dimensions'], row, col):
            if not game['mask'][nr][nc]:
                game['mask'][nr][nc] = True
                count += dig(game, nr, nc)
    
    status = 'victory' if is_victory(game) else 'ongoing' 
    game['state'] = status
    return count


def render(game, xray=False):
    nrows, ncols = game['dimensions']
    board = game['board']
    return [['_' if (not xray) and (not game['mask'][r][c]) else
             ' ' if board[r][c] == 0 else str(board[r][c])
             for c in range(ncols)] for r in range(nrows)]


def render_ascii(game, xray=False):
    return "\n".join((("%s"*len(r)) % tuple(r)) for r in render(game, xray=xray))
