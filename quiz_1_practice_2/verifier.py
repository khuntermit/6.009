import traceback

def verify( result, input_data, gold ):
  if result[0] == 'error':
    return False,result[1]
  result = result[1]
  
  try:
    ok =  (result == gold)
    message = "isn't right :(, your code produces %s" % str(result)
    if ok:
      message = "looks good, yay!"
  except:
    print(traceback.format_exc())
    ok = False
    message = "CRASHED! :(. See above for details."
  return ok, message
