import traceback

def verify(result, input_data, gold):
    try:
        if (input_data["function"] == "get_near_classes"):
            ok = (sorted(result) == sorted(gold))
        elif (input_data["function"] == "get_class_buildings"):
            # Result should be a list of lists
            is_list_of_lists = True
            if type(result) is not list:
                is_list_of_lists = False
            else:
                for x in result:
                    if (type(x) is not list):
                        is_list_of_lists = False
                        break
            if not is_list_of_lists:
                ok = False
                message = "result should be a list of lists of pairs! :("
            elif (len(result) != len(gold)):
                ok = False
                message = "result is not of correct length :("
            else:
                result2 = []
                for item in result:
                    result2.append(sorted(item))
                gold2 = []
                for item in gold:
                    gold2.append(sorted(item))
                ok = (sorted(result2) == sorted(gold2))
        else:
            ok = (result == gold)
        if ok:
            message = "looks good, yay!"
    except:
        print (traceback.format_exc())
        ok = False
        message = "CRASHED! :(. See above for details."
    if ok:
        message = "looks good, yay!"
    else:
        if type(result) == list and result[0] == 'error':
            message = str(result[1])
        else:
            message = "isn't right :(, your code produces %s" % str(result)

    return ok, message
