import quiz, json, traceback

# We can't JSON encode "trees" with fancy DAG structure, as for the last problem
# on this quiz.  Instead, we work with arrays of nodes, with pointers replaced by
# numeric indices.  This function translates back to proper trees.
def make_tree(tarray):
  if len(tarray) == 0:
    return None

  outarray = [{"data": v["data"], "left": None, "right": None, "prev": None, "next": None}
              for v in tarray]
  for i in range(len(tarray)):
    def fixupField(field):
      index = tarray[i][field]
      if index != None:
        outarray[i][field] = outarray[index]

    fixupField("left")
    fixupField("right")
    fixupField("prev")
    fixupField("next")

  return outarray[0]

# Next, a function to reverse that last transformation.
def unmake_tree(tree):
  tarray = []
  # We build up the flattened version here.

  index_by_id = {}
  # Maps node ID to index within tarray.

  # First pass: create just the tree structure within the array
  def make_skeleton(tree):
    if tree:
      index = len(tarray)
      index_by_id[id(tree)] = index
      node = {"data": tree["data"], "prev": tree["prev"], "next": tree["next"]}
      tarray.append(node)
      node["left"] = make_skeleton(tree["left"])
      node["right"] = make_skeleton(tree["right"])
      return index

  make_skeleton(tree)

  # Second pass: fix up the prev and next pointers.
  for node in tarray:
    def fixupField(field):
      if node[field] != None:
        node[field] = index_by_id[id(node[field])]
    fixupField("prev")
    fixupField("next")

  return tarray

def run_test( input_data ):
  result = ""
  try:
    name = input_data["function"]
    f = getattr(quiz, name)
    inputs = input_data["inputs"]

    if name in {"all_between", "insert"}:
      tree = make_tree(inputs["tree"])
      inputs["tree"] = tree

    result = f(**inputs)

    if name == "insert":
      result = unmake_tree(tree)
  except:
    return ('error', traceback.format_exc())
  return ('ok', result)
