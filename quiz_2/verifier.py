import traceback


def verify( result, input_data, gold ):
  if result[0] == 'error':
    return False, result[1]
  result = result[1]

  # Ok until we see otherwise...
  ok = True
  message = "looks good, yay!"

  try:
    if input_data['function'] == 'check_BST':
        ok = False
        message = "isn't right :(, your code produces %s" % str(result)
        ok =  (result == gold)
        if ok:
          message = "looks good, yay!"
    
    if input_data['function'] == 'pipe_cutting':
        ok = False
        message = "isn't right :(, your code produces %s" % str(result)
        ok =  (result == gold)
        if ok:
          message = "looks good, yay!"

    if input_data['function'] == "alternating_colors":
        ok = True
        message = "looks good, yay"
        if (result == {} and gold == True) \
           or (result != {} and gold == False):
            ok = False
            message = "isn't right :(, your code produces %s" % str(result)
        elif result != {} and gold == True:
            #Need to check that a valid coloring was returned in result
            for vertex in result.keys():
                if result[vertex] != 'Red' and result[vertex] != 'Blue':
                    ok = False
                    message = "isn't right :(, illegal color in %s" % str(result)
            graph = input_data["inputs"]["graph"]
            for vertex in graph.keys():
                if vertex not in result:
                    ok = False
                for dest in graph[vertex]:
                    if result[vertex] == result[dest]:
                        #violated rule
                        ok = False
                        message = ("isn't right :(, adjacent vertices %s and %s" + \
                                  "have the same color") %(str(vertex), str(dest))

  except:
    print(traceback.format_exc())
    ok = False
    message = "CRASHED! :(. See above for details."
  return ok, message
