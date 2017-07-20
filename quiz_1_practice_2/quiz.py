# Problem 1
# ---------
def median( A ):
    length = len(A)
    A.sort()
    if length % 2 == 0:
        index2 = int(length / 2)
        index1 = index2 - 1
        return (A[index1] + A[index2])/2
    index = int(length/2)
    return A[index]

# Problem 2
# ---------
def is_quasidrome( s ):
    forward = s
    reverse = s[::-1]
    diff = 0
    for i in range(len(s)):
        if forward[i] != reverse[i]:
            diff += 1
    if diff == 0 or diff == 1:
        return True
    return False

# Problem 3
# ---------
def is_permutation( A, B ):
    def create_dict(word):
        word_letters = {}
        for index in range(len(word)):
            letter = word[index]
            if letter not in word_letters:
                word_letters[letter] = 1
            else:
                word_letters[letter] += 1
        return word_letters

    A_letters = create_dict(A)
    B_letters = create_dict(B)
    for let in A_letters:
        if let not in B_letters:
            return False
        elif A_letters[let] != B_letters[let]:
            return False
    return True

# Problem 4
# ---------
def count_triangles( edges ):

    if len(edges) < 3:
        return 0

    nodes = []
    for edge in edges:
        for point in edge:
            if point not in nodes:
                nodes.append(point)
    return 1

# Problem 5
# ---------
def eval_ast(ast):
    """
    AST_1 = { "node":   "*",
                  "left":   { "node": "+",
                              "left": { "node": 3 },
                              "right": { "node": 2 } },
                  "right":   { "node": "*",
                              "left": { "node": 2 },
                              "right": { "node": 4 } }
                }
    """
    def find_val(dict, left, right):
        if len(dict) > 1:
            if type(dict) is str:
                if
                if key == "left":
                    left = dict["left"]
                if key == "right":
                    right = dict["right"]



