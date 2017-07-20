# 6.009 Quiz 2, Fall 2016

# NOTE: NO IMPORTS ALLOWED!

####################################################
##  Problem 1. Prairie Dog Housing Lottery
####################################################

# Please implement the function lottery(prairie_dogs, capacities), which assigns
# prairie dogs to available burrows.  Not all prairie dogs are willing to live
# in all burrows; they have idiosyncratic individual preferences.  Furthermore,
# each borrow can only fit so many prairie dogs.  The first input value is a
# list with one element per prairie dog, where each element is itself a list of
# numbers, each number standing for an available burrow.  The second input value
# is a list giving burrow capacities.  Indices in this list correspond to
# numbers from the prairie-dog-preference lists.
#
# If an assignment exists from prairie dogs to burrows, satisfying everyone's
# preferences, then return that assignment, as a list of numbers, following
# the same order as the original list.  If no satisfactory assignment exists,
# return None.
def lottery(prairie_dogs, capacities):
    capacity = 0
    for c in capacities
        capacity += c
    if len(prairie_dogs) > capacity:
        return None



####################################################
##  Problem 2. Advanced Forestry
####################################################

# A helpful function to create an initial tree with one data node.
def one_node_tree(data):
    return {"data": data, "left": None, "right": None, "prev": None, "next": None}

# You may find this function helpful to print trees while debugging.
def print_tree(tree):
    def tweak_indent(indent):
        if indent == "":
            return "|_"
        else:
            return "  " + indent

    def print_tree_indented(prefix, tree, indent):
        if tree == None:
            return

        print(indent + prefix + " " + str(tree["data"]))
        if tree["prev"]:
            print(indent + "Prev: " + str(tree["prev"]["data"]))
        if tree["next"]:
            print(indent + "Next: " + str(tree["next"]["data"]))

        print_tree_indented("Left:", tree["left"], tweak_indent(indent))
        print_tree_indented("Right:", tree["right"], tweak_indent(indent))

    print_tree_indented("Root:", tree, "")

# Given a tree of the kind explained in the readme, modify it to add the new
# data value.
def insert(tree, data):
    raise NotImplementedError
