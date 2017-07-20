# NO IMPORTS!

####QUESTIONS####

# Problem 1
# ---------
# The code determines if a graph can be colored using two colors or not.
# Return {} if the graph cannot be colored. 
# Return coloring_dict if the graph can be colored, where the coloring_dict
# maps vertices in the graph to "Red" or "Blue"

# def alternating_colors(graph, start, color_dict={}):
#     for i in range(len(graph)):
#         color_dict[start] = 'Red'
#         children = graph[start]
#         for child in children:
#             color_dict[child] = "Blue"
#     return {}

"""
I knew I had to traverse the graph but didn't know how.
In the revision I use breadth first search and mark each level with alternating colors.
I check at each marking if the nodes had already been colored, and check if the colors match.
"""


def alternating_colors(graph, start):
    """Do a breadth-first search on the graph. 
    At every even depth, color the nodes one color, 
    say red, and at the odd-depths, you color the nodes blue. 
    Every time you have a non-tree edge 
    (an edge between two nodes you have already visited) 
    verify that the colors are different. If the graph has several 
    connected components, you just repeat the search on each component."""
    visited = [start]
    this_level = graph[start]
    color = "Red"
    color_dict = {start: color}

    while this_level:
        # track the levels for coloring
        next_level = []
        # alternates color
        color = assign_color(color)

        # iterates through entire level in queue
        for q in range(len(this_level)):
            node = this_level.pop(0)

            # checks if the node is already a different color
            if node in visited:
                if color is not color_dict[node]:
                    return {}

            # assigns color
            color_dict[node] = color

            # adds children to queue
            children = graph[node]
            for child in children:
                if child not in visited:
                    next_level.append(child)

            # marks node as visited
            visited.append(node)

        # advances the queue
        this_level = next_level

    return color_dict


# swaps color between red and blue
def assign_color(parent_color):
    if parent_color is "Red":
        return "Blue"
    return "Red"

# Problem 2
# ---------
# Given a binary tree, check if it is a Binary Search Tree (BST).
# In a BST, for every vertex, the value of the vertex is greater than the
# value of any vertex in its left subtree, and less than the value of any
# vertex in its right subtree.
# Return True or False depending on whether tree is a BST or not.

# if start is '':
#     return True
# node = btree[start]
# if node[1] is '' and node[2] is '':
#     return True
# if node[1] is '':
#     if node[2] > node[0]:
#         return check_BST(btree, node[2])
#     return False
# if node[2] is '':
#     if node[1] < node[0]:
#         return check_BST(btree, node[1])
#     return False
# return False

"""
In my first attempt, I tried doing a recursive traversal.
In the revision, I fixed it and made it an in-order traversal.
I stored the values in a list and checked if the list was in order.
"""

def check_BST(btree, start):
    # traverses tree in-order and returns a list
    def inorderTraversal(btree, start):
        res = []
        if len(start) > 0:
            res = inorderTraversal(btree, btree[start][1])
            res.append(btree[start][0])
            res = res + inorderTraversal(btree, btree[start][2])
        return res

    ans = inorderTraversal(btree, start)

    # checks that the list is in order
    return all(ans[i] <= ans[i + 1] for i in range(len(ans) - 1))

# Problem 3
# ---------
# Return minimum number of pipes of length stock_length
# that can be cut to satisfy the list of requested

# def pipe_cutting(requests, stock_length, pipe=0, num_pipes=0):
#     if len(requests) == 0:
#         return num_pipes
#     if pipe + requests[0] < stock_length:
#         return pipe_cutting(requests[1:], stock_length, pipe + requests[0], num_pipes)
#     if pipe + requests[0] >= stock_length:
#         return pipe_cutting(requests[1:], stock_length, 0, num_pipes+1)

"""
In my original, I managed to get a recursive solution working, but it didn't optimize 
the number of pipes needed. In my revision, I check if the requested pipes fit into a 
certain number of stock pipes starting at 0. If they don't fit, I increase the number
of pipes until I reach a solution, ensuring that I always get the minimum as my solution.
"""


def solve(requests, material):
    """
    Determines if requests can fit into pipes provided. Returns True or False.
    """
    # pipes fit
    if len(requests) == 0:
        return True

    # not enough material
    if len(material) == 0:
        return False

    # takes a new piece of material to work with
    piece = material.pop(0)

    # the object of my for loop is being modified, so I needed a way to adjust the indexes
    # so I wouldn't have an out-of-bounds error
    minus = 0

    for i in range(len(requests)):
        # checks that piece fits in stock pipe
        if piece - requests[i + minus] >= 0:
            # removes pipe from stock
            piece -= requests[i + minus]
            # removes request from list
            requests.pop(i + minus)
            # request length decreases by 1, must account for that in indexes
            minus -= 1

    # continue process until stock or requests run out
    return solve(requests, material)


def pipe_cutting(requests, stock_length):
    ans = False
    num_pipes = -1

    # must fit largest pipes first
    requests.sort()
    requests.reverse()

    material = []

    # will only exit loop if requests fit the number of pipes
    while ans is False:

        # increments pipes
        num_pipes += 1
        ans = solve(requests, material)
        # increases the materials given by 1
        material.append(stock_length)

    return num_pipes



