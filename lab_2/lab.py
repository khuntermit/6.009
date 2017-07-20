def did_x_and_y_act_together(data, actor_id_1, actor_id_2):
    for pairs in data:
        # checks if actor1 and actor2 is present in the list
        if set([actor_id_1, actor_id_2]).issubset(set(pairs)):
            return True
    return False

# makes a dictionary
# key: actor, value: set of every actor the person has acted with
def data_structure(data):
    dict_data = {}
    for actor in data:
        # if actor is already in the new dictionary, add a value to its set
        if actor[0] in dict_data:
            dict_data[actor[0]].add(actor[1])
        # if actor is not present in the new dictionary
        else:
            dict_data[actor[0]] = {actor[1]}
    return dict_data

# returns an ordered list of actors with bacon number n
def get_actors_with_bacon_number(data, n):
    dict_data = data_structure(data)
    already_numbered = set()
    bacon_number = {4724}
    # repeats process n times
    for n in range(n):
        # keeps a record of all of the actors in previous bacon numbers
        for i in bacon_number:
            already_numbered.add(i)
        # creates new set of people with bacon number n+1
        bacon_number = next_bacon_number(dict_data, bacon_number, already_numbered)
    # turns set to list and sorts
    list_bacon_number = list(bacon_number)
    list_bacon_number.sort()
    return list_bacon_number


def next_bacon_number(dict_data, bacon_number, already_numbered):
    next_number = set()
    for n in bacon_number:
        temp_set = dict_data[n]
        # goes through actors who acted with people in the old bacon number
        for d in temp_set:
            # checks to not include people in previous bacon numbers
            if d in already_numbered:
                continue
            else:
                next_number.add(d)
    return next_number


def get_bacon_path(data, actor_id):
    dict_data = data_structure(data)
    # checks if actor id not present
    if actor_id not in dict_data:
        return None
    already_numbered = set()
    bacon_number = {4724}
    # a dictionary with the parent as value, child as key
    parents = {}
    # runs until the bacon number progresses to contain the actor
    while actor_id not in bacon_number:
        next_number = set()
        # goes through people in existing bacon number
        for n in bacon_number:
            temp_set = dict_data[n]
            # goes through everyone who acted with this actor
            for d in temp_set:
                # checks not to include people in previous bacon numbers
                if d in already_numbered:
                    continue
                else:
                    next_number.add(d)
                    # storing parenthood
                    parents[d] = n
        bacon_number = next_number
        already_numbered.update(bacon_number)
    return find_path(parents, actor_id)


def find_path(parents, actor_id):
    path = [actor_id]
    target = actor_id
    while target != 4724:
        target = parents[target]
        path.append(target)
    path.reverse()
    return path
