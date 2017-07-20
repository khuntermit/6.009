import lab, json, traceback
from importlib import reload
reload(lab) # this forces the student code to be reloaded when page is refreshed

def run_test( input_data ):
    try:
        # build trie, insert words
        trie = lab.Trie()
        words = input_data["words"]
        if words == 'jules_verne':
            with open("resources/words.json", "r") as f:
                words = json.load(f)
                for w in set(words):
                    trie.insert(w,words.count(w))
        else:
            for w in words:
                trie.insert(w)

        # select subtrie if requested
        if "find" in input_data:
            trie = trie.find(input_data["find"])

        # invoke method if asked to
        if "method" in input_data:
            f = getattr(trie, input_data["method"])
            if "args" in input_data:
                result = f(*input_data["args"])
            else:
                result = f()
        else:
            result = None

        # package result for verifier
        return ('ok',trie,result)
    except:
        return ('error',traceback.format_exc())

##################################################
## for server.py
##################################################

# global trie that holds resources/words.json
trie = None
def load_words():
    global trie
    if trie is not None: return

    # load json word list, insert into trie
    print("LOADING CORPUS")
    trie = lab.Trie()
    with open("resources/words.json", "r") as f:
        words = json.load(f)
        for w in set(words):
            trie.insert(w,words.count(w))

def autocomplete( input_data ):
    global trie
    load_words()
    return trie.autocomplete(input_data["prefix"], input_data["N"])

def autocorrect( input_data ):
    global trie
    load_words()
    return trie.autocorrect(input_data["prefix"], input_data["N"])

def init():
    # Nothing to initialize
    return None

init()
