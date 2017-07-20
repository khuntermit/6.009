# No imports allowed


def bad_ends(maze, dims, start, goal):
    """
    Checks if the start and goal are valid endpoints
    - not on an 'X', in bounds
    - start must be in the first row and end must be in the last row
    :param maze: 2D array default maze
    :param dims: array of the maze dimensions
    :param start: array coordinate of the start point
    :param goal: array coordinate of the goal point
    :return: True if the ends are bad, False if they are valid
    >>> maze = [["c", 0,  1,  1,  1,  0 ],[ 1, "c","c","c","c","b"],[ 0,  0,  0,  1,  1,  0 ],[ 1,  0,  1, "c", 1, "c"],[ 0, "c", 0, "c", 0,  0 ]]
    >>> bad_ends(maze, [5, 6], [4, 5], [0, 0])
    True
    """

    if valid_square(maze, dims, start) and valid_square(maze, dims, goal):
        if goal[0] > start[0]:
            return False
    return True


def dead_maze(dims):
    """
    If there is no valid path through the maze, returns a maze full of "X" in the specified dimensions
    :param dims: a list containing the maze dimensions
    :return: a maze of size dims full of "X"
    >>> dead_maze([2, 3])
    [['X', 'X', 'X'], ['X', 'X', 'X']]
    """
    return [['X' for col in range(dims[1])] for row in range(dims[0])]


def valid_square(maze, dimensions, coord):
    """
    Checks if the coord's row and col are in bounds and does not contain a 1
    :param maze: an array of arrays with structure corresponding to the rows of the maze where
            - 0 represents empty space
            - 1 represents a wall
            - "c" represents a coin
            - "b" represents a bomb
    :param dimensions: array containing dimensions of the maze
    :param coord: array coordinate to check if valid
    :return: True if the square is valid, False otherwise
    >>> maze = [["c", 0,  1,  1,  1,  0 ],[ 1, "c","c","c","c","b"],[ 0,  0,  0,  1,  1,  0 ],[ 1,  0,  1, "c", 1, "c"],[ 0, "c", 0, "c", 0,  0 ]]
    >>> valid_square(maze, [5, 6], [-1, 5])
    False
    >>> valid_square(maze, [5, 6], [0, 4])
    False
    >>> valid_square(maze, [5, 6], [1, 1])
    True
    """
    r = dimensions[0]
    c = dimensions[1]
    if 0 <= coord[0] < r and 0 <= coord[1] < c:
        if maze[coord[0]][coord[1]] is not 1:
            return True
    return False


def solve_maze(m, start, goal):
    """
    Find the paths from start to goal in a maze m that maximize the number of coins collected.

    :param m: a dictionary representing a maze with keys "dimensions" and "maze".
        > "dimensions" points to an array [nrows, ncols] corresponding to the dimensions of maze
        > "maze" points to an array of arrays with structure corresponding to the rows of the maze where
            - 0 represents empty space
            - 1 represents a wall
            - "c" represents a coin
            - "b" represents a bomb
    :param start: array in form [r, c]; starting point in the maze
    :param goal: array in form [r, c]; destination point in the maze
    :return: a dictionary result with the same structure as m
        where result["maze"][r][c], for 0<= r < nrows, 0<= c < ncols is
             "X" if no valid paths exist along path start --> (r, c) --> goal
             otherwise max number of coins collected on any valid path from start --> (r, c) --> goal
    """

    maze = m["maze"]
    dims = m["dimensions"]

    default = dead_maze(dims)
    paths = find_all_paths(maze, start, goal, dims)
    final = assign_values(maze, default, paths)
    m["maze"] = final
    return m


def assign_values(maze, default, paths):
    """
    Assigns values to the maze using a 2D array full of the paths
    :param maze: 2D array maze
    :param default: 2D array maze full of X
    :param paths: 3D array paths through the maze
    :return: 2D array final maze
    >>> assign_values([["c", 1,  1, 1], ["c", 0,  1, 1],[ 1, "c","c",1],[ 1,  1,  0, 0]], dead_maze([4, 4]), [[[0, 0], [1, 0], [1, 1], [2, 1], [2, 2], [3, 2], [3, 3]]])
    [[1, 'X', 'X', 'X'], [2, 2, 'X', 'X'], ['X', 3, 4, 'X'], ['X', 'X', 4, 4]]
    """
    for path in paths:
        path_sum = 0
        for point in path:

            r = point[0]
            c = point[1]

            if maze[r][c] is 'b':
                path_sum = 0
                if default[r][c] is 'X':
                    default[r][c] = 0

            if maze[r][c] is 'c':
                path_sum += 1
                if default[r][c] is 'X' or default[r][c] < path_sum:
                    default[r][c] = path_sum

            if maze[r][c] is 0:
                if default[r][c] is 'X' or default[r][c] < path_sum:
                    default[r][c] = path_sum

    return default


def get_next(node, dims, maze):
    """
    Gets the squares connected to the node
    :param node: array cell
    :param dims: array dimensions
    :param maze: 2D array maze
    :return: 0 - 2 length array representing cells connecting the node
    
    >>> maze = [["c", 0,  1,  1,  1,  0 ],[ 1, "c","c","c","c","b"],[ 0,  0,  0,  1,  1,  0 ],[ 1,  0,  1, "c", 1, "c"],[ 0, "c", 0, "c", 0,  0 ]]
    >>> get_next([0, 0], [5, 6], maze)
    [[0, 1]]
    >>> get_next([1, 1], [5, 6], maze)
    [[2, 1], [1, 2]]
    """
    r = node[0]
    c = node[1]
    connected = []
    if valid_square(maze, dims, [r + 1, c]):
        connected.append([r + 1, c])
    if valid_square(maze, dims, [r, c + 1]):
        connected.append([r, c + 1])
    return connected


def find_all_paths(maze, start, end, dims, path=[]):
    """    
    :param maze: 2D maze
    :param start: array start coord
    :param end: array end coord
    :param dims: array dimensions of maze
    :param path: array path through the maze
    :return: paths through maze
    
    >>> find_all_paths([["c", 1,  1, 1], ["c", 0,  1, 1],[ 1, "c","c",1],[ 1,  1,  0, 0]], [0, 0], [3, 3], [4, 4])
    [[[0, 0], [1, 0], [1, 1], [2, 1], [2, 2], [3, 2], [3, 3]]]
    """
    path = path + [start]
    if start == end:
        # reached destination, return a list containing this path
        return [path]
    # start a list of paths that we discover
    paths = []
    for node in get_next(start, dims, maze):
        if node not in path:
            # continue path finding with neighbor.
            # accumulate list of paths that we find
            paths.extend(find_all_paths(maze, node, end, dims, path))
    return paths


def pretty_print(m):
    """
    Prints a visual representation of a maze (useful for debugging)
    :param m: maze
    """
    nrows, ncols = m["dimensions"]
    print("\n > Dimensions: ", m["dimensions"], "\n")
    print(" " + "-" * 3 * ncols)
    for r in range(nrows):
        line = ""
        for c in range(ncols):
            elt = m["maze"][r][c]
            if c == 0:
                line += "|"
            if type(elt) == int:
                if elt >= 10:
                    line += " " + str(elt)
                else:
                    line += " " + str(m["maze"][r][c]) + " "
            else:
                line += " " + str(m["maze"][r][c]) + " "
            if c == ncols - 1:
                line += "|"
        print(line)
    print(" " + "-" * 3 * ncols + "\n")

