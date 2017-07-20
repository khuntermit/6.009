import traceback

def verify( result, input_data, gold ):
  if result[0] == 'error':
    return False, result[1]
  result = result[1]

  # Ok until we see otherwise...
  ok = True
  message = "looks good, yay!"

  try:
    if input_data['function'] == 'maxSubsequence':
      if result[0] <= result[1]:
        # for regular max_subseq
        result_sum = sum([x for i,x in enumerate(input_data["inputs"]["ilist"]) if i >= result[0] and i <= result[1]])
      else:
        # for circular max_subseq
        result_sum = sum([x for i,x in enumerate(input_data["inputs"]["ilist"]) if i <= result[1] or i >= result[0]])
      ok =  (result_sum == gold)
      if not ok:
        message = "isn't right :(, your code produces {0} summing to {1}".format(str(result), str(result_sum))
    
    if input_data['function'] == 'findTriple':
      if result == None:
        result_verify = False
      else:
        x = result[0]
        y = result[1]
        z =  x + y
        s = input_data["inputs"]["ilist"] #keep as a LIST to account for duplicates
        # Note: the code below allows [175, 175] which for case 4.in IS a valid
        # triplet according to the spec, since 175 is repeated in the input list
        # and 350 is also in the input list.
        result_verify = False
        if x in s:
          #remove x from x
          s.remove(x)
          if y in s:
            #remove y from x
            s.remove(y)
            if z in s:
              result_verify = True
      ok = (result_verify == gold)
      if not ok:
        message = "isn't right :(, your code produces %s" % str(result)
    
    if input_data['function'] == 'findPath':
      if result == None:
        if gold: # there is a path
          ok = False
          message = "isn't right :(, your code produces %s" % str(result)
      else:
        path = result
        grid = input_data["inputs"]["grid"]
        
        try:
          prev_coord = None
          for i in range(len(path)):
            if i == 0:
              prev_coord = path[0]
              if grid[prev_coord[0]][prev_coord[1]] != 1:
                result_verify = None
                break

            coord_row = path[i][0]
            coord_col = path[i][1]
            if grid[coord_row][coord_col] == 1 and abs(prev_coord[1] - coord_col) <= 1 \
               and 0 <= coord_col and coord_col <= len(grid[0]) \
               and 0 <= coord_row and coord_row <= len(grid):
                prev_coord = path[i]
            else:
              result_verify = None
              break

            if i == len(grid)-1:
              result_verify = True
          ok = result_verify == gold
          if not ok:
            message = "isn't right :(, your code produces %s" % str(result)
        except:
          ok = False
          message = "isn't right :(, your code produces %s" % str(result)

  except:
    print(traceback.format_exc())
    ok = False
    message = "CRASHED! :(. See above for details."
  return ok, message
