import traceback, json


# Checks if a path is valid.
def validate_path(data, path):

        # If the path is None, it's valid.
        if path is not None:

                # Check for length (We need at least one node for a path)
                if len(path) < 1:
                        return False

                # Special case - path length 0
                if len(path) == 1:
                        return path[0] in data

                # Check that all nodes are connected sequentially
                for i in range(0, len(path) - 1):
                        # Check if the node exists
                        if path[i] not in data:
                                return False
                        else:
                                # If it does, checks if it connected to the following one
                                if path[i + 1] not in data[path[i]]:
                                        return False
        return True


def convert(data_set):
        graph = {}
        for pair in data_set:
                if pair[0] not in graph:
                        temp = set()
                        temp.add(pair[1])
                        graph[pair[0]] = temp
                else:
                        graph[pair[0]].add(pair[1])
        return graph


# Verifies if the path is valid and correct
def check_path(result, input_data, gold, data):

        # If the answer is None, just compare to the gold
        if result is None:
                return gold is None
        else:
                # Checks id the path is valid
                if validate_path(convert(data), result):
                        # Check if the end nodes are correct, and if the length is shortest one
                        start_node = 4724  # Kevin Bacon
                        end_node = input_data['actor_id']

                        return result[0] == start_node \
                                        and result[-1] == end_node \
                                        and len(result) - 1 == gold
        return False


def verify(result, input_data, gold):

        running_time,result = result
        if running_time == 'error' or isinstance(result,str):
                return False, result

        gold_time = 30.0

        ok, message = True, "something is odd, there is no feedback given :|"

        try:
                if float(running_time) <= float (gold_time):
                        if input_data["function"] == "pair":
                                message = "Oh no, seems like you did the wrong match..."
                        elif input_data["function"] == "set":
                                message = "Oh no, seems like your list is incorrect... is the list sorted?"
                        if input_data["function"] == "path_small":
                                ok = check_path(result, input_data, gold, small_data)
                                message = "Oh no, the path is incorrect"
                        elif input_data["function"] == "path":
                                ok = check_path(result, input_data, gold, large_data)
                                message = "Oh no, the path is incorrect"
                        else:
                                ok = (result == gold)

                        if ok:
                                message = "Good job! your answer is correct (%f seconds)" % float(running_time)
                else:
                        ok, message = False, "Your code is too slow (%f seconds)... check your data structures and general approach..." % float(running_time)

        except:
                print(traceback.format_exc())
                ok = False
                message = "your code could not be verified :(. Stack trace is printed above so you can debug."
        return ok, message


small_data = None
large_data = None


def init():
        global small_data
        global large_data
        with open('resources/small.json', 'r') as f:
                small_data = json.load(f)
        with open('resources/large.json', 'r') as f:
                large_data = json.load(f)
        return


init()
