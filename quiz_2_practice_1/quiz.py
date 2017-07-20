# Problem 1
# ---------
def check_valid_paren(s):
    count = 0
    for ch in s:
        if ch == '(':
            count += 1
        elif ch == ')':
            count -= 1
        if count < 0: return False
    return count == 0


# Problem 2
# ---------
def solve_latin_square(grid):
    return "Implement Me!"




# Problem 3
# ---------
def is_proper(root):
    return "Implement Me!"

