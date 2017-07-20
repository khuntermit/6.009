# NO IMPORTS!

####QUESTIONS####

# If the list ilist contains three values x, y, and z such that x + y = z
# return a tuple with x and y. Otherwise return None.
def findTriple(ilist):
    """
    `findTriple([4,5,9])` should return `(4,5) or (5,4)`.

    `findTriple([20,40,100,50,30,70])` should return `(30,70) or (70,30)` or `(20,50) or (50,20)` or `(20,30) or (30,20)`.

    `findTriple([6,11,7,2,3])` should return `None`.
    """
    # Set for efficiency
    set_ilist = set(ilist)
    for x in range(len(ilist)):
        for y in range(len(ilist)):
            if x != y:
                val = ilist[x] + ilist[y]
                if val in set_ilist:
                    return ilist[x], ilist[y]
    return None
    
# Return the start and end indices as a tuple of the maximum subsequence
# in the list.  If is_circular = True, imagine the list is circular.
# That is, after the end index comes the start index. 
def maxSubsequence(ilist, is_circular = False):

    # Original *********************************************************************************
    # def rec_sub(ilist, length, circular, max_sub_start=0, max_sub_finish=0, max_sum=0):
    #     if len(ilist) > 800:
    #         return (42, 43)
    #     for i in range(len(ilist)):
    #         current_sum = ilist[i]
    #         for j in range(i + 1, len(ilist)):
    #             current_sum += ilist[j]
    #             if current_sum > max_sum:
    #                 max_sum = current_sum
    #                 max_sub_start = i
    #                 max_sub_finish = j
    #         return (max_sub_start, max_sub_finish)
    #
    # l = len(ilist)
    # return rec_sub(ilist, l, is_circular)
    # ***********************************************************************************

    # This question only required minor changes. I had most of the internal structure right
    # except I made a couple mistakes on my start and stop indexes shown below.

    if is_circular:
        ilist = ilist + ilist

    max_sum_finish = 0
    max_sum_start = 0
    max_sum = ilist[0]

    # Small bug was here - my start index was moving past the non-circular length of ilist
    # Re-specified start ranges for both circular and non-circular conditions
    if is_circular:
        start = len(ilist)//2
    else:
        start = len(ilist)

    for i in range(start):
        current_sum = ilist[i]
        # Small bug was here - my end index was moving beyond the circular length
        # Re-specified end ranges for both circular and non-circular conditions
        if is_circular:
            end = (len(ilist)//2) + i
        else:
            end = len(ilist)

        for j in range(i + 1, end):
            current_sum += ilist[j]
            if current_sum > max_sum:
                max_sum = current_sum
                max_sum_start = i
                max_sum_finish = j

    if is_circular:
        # Finish index is the remainder of the index / non-circular length of ilist
        max_sum_finish %= len(ilist)//2

    return max_sum_start, max_sum_finish


# Given a two dimensional n by m grid, with a 0 or a 1 in each cell,
# find a path from the top row (0) to the bottom row (n-1) consisting of
# only ones.  Return the path as a list of coordinate tuples (row, column).
# If there is no path return None.
def findPath(grid):

    # Origial ****************************************
    #
    # list = []
    # for x in range(len(grid)):
    #     for y in range(len(grid[0])):
    #         t = (x, y)
    #     list.append(t)
    # all_coords = every_path(list)
    #
    # answers = []
    # for coord in all_coords:
    #
    #     for ind in range(len(coord)):
    #         row = grid[ind]
    #         if row[coord[ind]] != 1:
    #             continue
    #         if coord not in answers:
    #             answers.append(coord)
    # return answers
    # Original ********************************************

    # Completely flipped this problem - at first attempted to try every path which would have been costly.
    # Switched to depth-first search

    # Returns a list containing the locations of the 1s as tuples
    def find_ones(grid):
        ones = []
        for row in range(len(grid)):
            for ind in range(len(grid[0])):
                if grid[row][ind] == 1:
                    ones.append((row, ind))
        return ones

    # Creates a dictionary storing parent:children
    def adj_dict(ones):
        adjacent = {}
        for parent in ones:
            daughters = []
            for daughter in ones:
                # Row condition
                if daughter[0] == parent[0] + 1:
                    # Column condition
                    if parent[1] - 1 <= daughter[1] <= parent[1] + 1:
                        daughters.append(daughter)
            adjacent[parent] = daughters
        return adjacent

    # creates lists containing start and end points
    def target_lists(ones, target):
        list = []
        for one in ones:
            if one[0] == target:
                list.append(one)
        return list

    # Finds the path
    def find_path(start, end, adjacent):
        # Goes through each start coord
        for s in start:
            queue = [s]
            # Stores path movements - child:parent
            parents = {}
            while queue:
                # Takes the last element off the queue
                element = queue.pop()
                # End condition - if the queued element is found in the end list
                if element in end:
                    # Backtracks - builds the path backwards
                    path = [element]
                    # Builds until it hits the beginning
                    while element not in start:
                        element = parents[element]
                        path.append(element)
                    # Reverses the path so it faces the right direction
                    path.reverse()
                    return path

                for adj in adjacent[element]:
                    # Adds the following elements to the queue
                    queue.append(adj)
                    # Stores path movements
                    parents[adj] = element

    ones = find_ones(grid)
    adjacent = adj_dict(ones)
    # Coords of the 1s in the first row
    start = target_lists(ones, 0)
    # Coords of the 1s in the last row
    end = target_lists(ones, len(grid) - 1)
    return find_path(start, end, adjacent)

###Tests###
