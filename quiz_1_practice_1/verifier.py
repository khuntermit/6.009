import traceback

def verify( result, input_data, gold ):
  try:
    ok =  (result == gold)
    message = "isn't right :(, your code produces %s" % str(result)
    if ok:
      message = "looks good, yay!"
  except:
    print(traceback.format_exc())
    ok = false
    message = "CRASHED! :(. See above for details."
  return ok, message
