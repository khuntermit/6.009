import traceback

# Checks to see if student output satisfies constraints
def verify_latin_square (result, gold, grid):
    if (not gold and not result):
        return True, "Your code correctly finds no solution"
    if isinstance(result,str):
        return False,result

    try:
        # Check that output is proper size
        length = len(grid)
        if not isinstance(result, list) or len(result) != length:
            return False, "Grid of incorrect dimensions or type"
        for row in result:
            if isinstance(row, (int, float)) or len(row) != length:
                return False, "Grid of incorrect dimensions or type"
        # Check that the given grid elements are the same
        for r in range(length):
            for c in range(length):
                if grid[r][c] != -1 and result[r][c] != grid[r][c]:
                    return False, "You changed the given grid values"
        # Check that rows/columns contain numbers 1, 2, ...n
        for r in range(length):
            row = [result[r][c] for c in range(length)]
            if sorted(row) != list(range(1, length + 1)):
                return False, "row/column does not coontain 1, 2, ..., n"
        for c in range(length):
            column = [result[r][c] for r in range(length)]
            if sorted(column) != list(range(1, length + 1)):
                return False, "row/column does not coontain 1, 2, ..., n"
        return True, "looks good!"
    except:
        return False, "your result is very wrong :("

def verify( result, input_data, gold ):
  if result[0] == 'error':
    return False, result[1]
  result = result[1]

  try:
    ok = False
    message = "isn't right :(, your code produces %s" % str(result)
    if (input_data["function"] == "solve_latin_square"):
        ok, message = verify_latin_square(result, gold, input_data["inputs"]["grid"])
    else:
        ok =  (result == gold)
    if ok:
      message = "looks good, yay!"
  except:
    print(traceback.format_exc())
    ok = False
    message = "CRASHED! :(. See above for details."
  return ok, message
