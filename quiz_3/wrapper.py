import quiz, json, traceback

def run_test( input_data ):
  result = ""
  try:
    f = getattr(quiz, input_data["function"])
    try:
        args = input_data["inputs"]
    except KeyError:
        args = {key: input_data[key] for key in input_data["argNames"]}
    if input_data["function"] != "count_straights":
        default_db, update_db = load_database()
        rep = quiz.build_rep(default_db, update_db)
        args["rep"]  = rep
        result = f(**args)
    else:
        result = f(**args)
  except:
        result = ('error',traceback.format_exc())
  return result

def load_database():
    with open("resources/database/default_db.txt") as f:
        default_db = [line.split() for line in f.read().split("\n") if len(line) > 0]
    with open("resources/database/update_db.txt") as f:
        update_db = [line.split() for line in f.read().split("\n") if len(line) > 0]
    return default_db, update_db
