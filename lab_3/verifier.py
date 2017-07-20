import traceback

MESSAGE = {
    "testdoc": "There's something wrong with the doctests...",
    "new_game": "Oh no, new_game isn't working correctly...",
    "dig": "Oh no, dig seems to be wrong...",
    "render": "Oh no, render isn't quite right...",
    "render_ascii": "Oh no, there's something wrong with render_ascii...",
    "integration_2d": "Oh no, combining multiple operations doesn't work quite right...",
}

def verify_helper(running_time, result, input_data, reference):
    TIME_LIMIT = 1.0

    try:
        if float(running_time) >= float(TIME_LIMIT):
            return False, "Your code is too slow... Check your data structures and general approach."

        test_test = False
        if isinstance(reference, dict) and 'correct' and 'incorrect' in reference:
            test_test = True
            try:
                result = {k: set(v) for k,v in result.items()}
                reference = {k: set(v) for k,v in reference.items()}
            except:
                pass
        ok = (result == reference)
        if ok:
            message = "Good job! Everything looks fine."
        else:
            message = MESSAGE.get(input_data["function"], None)
            if message is None:
                if test_test:
                    message = '\nReported Correct Implementations: %r\nExpected Correct Implementations: %r'
                    message %= (sorted(result.get('correct', [])), sorted(reference.get('correct', [])))
                else:
                    message = str(result)
        return ok, message
    except:
        print(traceback.format_exc())
        return False, "Your code could not be verified :( Stack trace is printed above so you can debug."

def verify(output, input_data, gold):
    running_time, result = output

    if running_time is None:
        return False, result

    return verify_helper(running_time, result, input_data, gold)
