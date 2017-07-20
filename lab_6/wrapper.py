import lab, json, traceback
from importlib import reload

reload(lab)  # this forces the student code to be reloaded when page is refreshed


def run_test(input_data):
    result = ""
    try:
        f = getattr(lab, input_data["function"])
        result = f(**input_data["inputs"])
    except:
        result = traceback.format_exc()
    return result
