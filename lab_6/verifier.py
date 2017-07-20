import traceback

def verify(result, input_data, goal):
    ok = True
    try:
        if type(result) != dict:
            message = "didn't work :( " + str(result)
            ok = False
        elif ("dimensions" not in result)  or ("maze" not in result):
            message = "didn't work :( Your code outputs something a dictionary with incorrect keys!"
            ok = False
        else:
            ok = ok and (result["dimensions"] == goal["dimensions"])
            ok = ok and (len(result["maze"]) == len(goal["maze"]))
            for row in result["maze"]:
                ok = ok and len(row) == goal["dimensions"][1]

            if not ok:
                message = "isn't right :( The dimensions of your output are not correct!"
            else:
                errors = 0
                nrows, ncols = goal["dimensions"]
                for r in range(nrows):
                    for c in range(ncols):
                        if result["maze"][r][c] != goal["maze"][r][c]:
                            errors += 1
                            ok = False
                message = "isn't right :( There are " + str(errors) + " incorrect squares in your result!"

            if ok:
                message = "is correct. Hooray!"
    except:
        traceback.print_exc();
        ok = False
        message = "crashed :( Stack trace is printed above so you can debug."

    return ok, message
