import quiz, json, traceback

def run_test( input_data ):
  result = ""
  try:
    f = getattr(quiz, input_data["function"])
    result = ('ok',f(**input_data["inputs"]))
  except:
    result = ('error',traceback.format_exc())
  return result
