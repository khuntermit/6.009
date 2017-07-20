# makes mask incorrectly (set to board not mask)
# dig is set to be int but then call index of it


def neighbors(dimensions, r, c):
    all_neighbors = [(r+i, c+j) for i in range(-1,2) for j in range(-1, 2)]
    return [(x,y) for (x,y) in all_neighbors if 0 <= x < dimensions[0] and 0 <= y < dimensions[1]]


def make_board(nrows, ncols, elem):
    return [[elem for c in range(ncols)] for r in range(nrows)]

# mask created is incorrect
def new_game(num_rows, num_cols, bombs):
    # here
    mask = make_board(num_rows, num_cols, False)
    board = make_board(num_rows, num_cols, 0) 
    for br, bc in bombs:
        board[br][bc] = '.'
    for br, bc in bombs:
        for nr, nc in neighbors([num_rows, num_cols], br, bc):
            if board[nr][nc] != '.':
                board[nr][nc] += 1
    # mask is set to board
    return {"dimensions": [num_rows, num_cols], "board" : board, "mask" : board, "state": "ongoing"}


def dig(game, row, col):
    # handle dig returns int
    def handle_dig(game, row, col, dig_count):
        recursion_count = 0
        if not game["mask"][row][col] and\
           type(game["board"][row][col]) == int:
            game["mask"][row][col] = True
            if game["board"][row][col] != 0:
                game['state'] = 'ongoing'
                return 1
            else:
                for offset1 in [-1,0,1]:
                    for offset2 in [-1,0,1]:
                        if row+offset1 >= 0 and row+offset1 < game["dimensions"][0] and \
                           col+offset2 >= 0 and col+offset2 < game["dimensions"][1]:
                            recursion_count += handle_dig(game, row+offset1, col+offset2, dig_count)[1]
                game['state'] = 'ongoing'
                return recursion_count + 1
        game['state'] = 'ongoing'
        return 0

    if game["board"][row][col] == ".":
        game["mask"][row][col] = True
        game['state'] = 'defeat'
        return 1

    if not game["mask"][row][col]:
        game["mask"][row][col] = True
    digger = handle_dig(game,row,col,0)
    
    bomb_count = 0
    for row in game["board"]:
        bomb_count += len([x for x in row if x == "."])
    revealed_count = 0
    for row in game["mask"]:
        revealed_count += len([x for x in row if x == True])

    if (game["dimensions"][0] * game["dimensions"][1]) - bomb_count == revealed_count:
        game['state'] = victory
        # here - call index of an int
        return digger[1]
    
    return digger


def render(game, xray=False):
    nrows, ncols = game['dimensions']
    board = game['board']
    return [['_' if (not xray) and (not game['mask'][r][c]) else
             ' ' if board[r][c] == 0 else str(board[r][c])
             for c in range(ncols)] for r in range(nrows)]


def render_ascii(game, xray=False):
    return "\n".join((("%s"*len(r)) % tuple(r)) for r in render(game, xray=xray))
