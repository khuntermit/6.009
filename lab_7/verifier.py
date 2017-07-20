import traceback

def dictify(trie,prefix=''):
    if trie is None: return None
    result = {"frequency": trie.frequency, "children": {}}
    for ch,child in trie.children.items():
        result["children"][ch] = dictify(child,prefix + ch)
    return result

def verify(xresult, input_data, gold):
    if xresult[0] == 'error':
        return False,xresult[1]
    result = xresult[2]

    ok = False
    try:
        if input_data.get("f") == "trie":
            result = dictify(xresult[1])
            ok = (result == gold)
            if not ok:
                message = "Your trie is incorrect."

        elif input_data.get("method") == "find":
            result = dictify(result)
            ok = (result == gold)
            if not ok:
                message = "Find returned an incorrect trie node."
                
        elif input_data.get("method") == "autocorrect":
            gold.sort()
            result.sort()
            ok = (result == gold)
            if not ok:
                message = "Your autocorrect results are incorrect."

        elif input_data.get("method") == "autocomplete":
            for answer in gold:
                answer.sort()
            result.sort()
            ok = (result in gold)
            if not ok:
                message = "Your autocomplete results are incorrect."

        elif input_data.get("method") == "__iter__":
            if isinstance(result,list):
                message = "__iter__ returned a list, not an iterator."
            else:
                result = sorted(list(result))
                ok = (result == gold)
                if not ok:
                    message = "Your iterator is incorrect."

        elif input_data.get("method") == "filter":
            result = sorted(result)
            ok = (result == gold)
            if not ok:
                message = "Your list of filtered words is incorrect."
                    
        else:
            ok = (result == gold)
            if not ok:
                message = "Your trie is incorrect."

        if ok:
            message = "is correct. Hooray!"
    except:
        print(traceback.format_exc())
        ok = False
        message = "crashed :(. Stack trace is printed above so you can debug."

    return ok, message
