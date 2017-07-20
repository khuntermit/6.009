
### Please refer to the Quiz 3 README for instructions. ###

### Problem 1 ###

def build_rep(default_db, update_db):
    # print(default_db)
    meetings = {}  # subj => list of (week, day, time)

    # start by processing default schedule to create complete
    # of meetings for each class
    for subj,hour,day,place in default_db:
        mlist = meetings.get(subj,[])
        meetings[subj] = mlist  # in case mlist is brand new
        for week in range(1,16):
            mlist.append((str(week), hour, day, place))

    # now process updates
    for action,subj,hour,day,place,week in update_db:
        # get list of meetings for this subj
        mlist = meetings.get(subj,[])
        meetings[subj] = mlist  # in case mlist is brand new
        # process udpate
        if action == 'DELETE':
            mlist.remove((week, hour, day, place))
        elif action == 'ADD':
            mlist.append((week, hour, day, place))

    return meetings


# OUTPUT: A list, in no particular order, of all classes that meet
# only in the list of buildings given by `buildings`.
def get_near_classes(buildings, rep):
    buildings = set(buildings)
    solution = list(rep.keys())
    for key, value in rep.items():
        for v in value:
            building = v[3]
            if building not in buildings and key in solution:
                solution.remove(key)
    return solution


# OUTPUT: An integer earliest time (hour, such as 9),
# the earliest meeting given by the combined database of classes,
# occurring on any week in `building` on `day_of_week`.
# If no meetings take place on `day_of_week` in that building on any
# week, return `None`.
def earliest_meeting(building, day_of_week, rep):
    earliest_hour = 17
    for key, value in rep.items():
        for v in value:
            hour = v[1]
            day = v[2]
            b = v[3]
            if day == day_of_week and b == building and int(hour) < earliest_hour:
                earliest_hour = int(hour)

    if earliest_hour == 17:
        return None
    return earliest_hour


# OUTPUT: A Boolean (True/False) indicating whether any two classes
# in class_list conflict. Two classes conflict when they meet on the same day
# of the week during the same week at the same time.
def have_conflicts(class_list, rep):
    if len(class_list) == 1:
        return False
    distinct_meetings = []
    for c in class_list:
        if c not in rep:
            continue
        classes = rep[c]
        for i in classes:
            distinct_meetings.append(i[:-1])
    compare = set(distinct_meetings)
    if len(compare) != len(distinct_meetings):
        return True
    return False

### Problem 2 ###
# Count the possible hands in k-Label Poker where
#    k = # labels
#    L = # levels, 1...L inclusive
#    n = number cards in a hand 
def count_straights(k, L, n):
    # I basically had to start from scratch on the resubmit because I had no idea what to do.

    # Step 1: Generate all possible cards
    levels = []
    for l in range(1, L + 1):
        levels.append(l)
    # List of ranges that reflects the dimensionality (range of labels repeats k times)
    ran_and_dims = [levels] * k

    # Step 2: Take the product of the lists for all the cards
    all_cards = nd_product(ran_and_dims)

    # Step 3: Weed out non-ascending cards
    asc = []
    for c in all_cards:
        s = list(c)
        if sorted(s) == s:
            asc.append(c)

    # Step 4: Recursively generate the number of straights that you can make
    # Valid stores all of the valid straights
    valid = []
    for a in asc:
        valid += find_all_straights(asc, a, n)
    return len(valid)


def find_all_straights(asc, card, n, straight=[]):
    """
    Given a starting card, returns all possible straights
    """

    straight = straight + [card]
    if len(straight) == n:

        return [straight]

    straights = []
    for c in range(len(asc)):
        if asc[c] not in straight and asc[c][0] >= card[-1] :

            straights.extend(find_all_straights(asc, asc[c], n, straight))
    return straights


def nd_product(sequence):
    """Produces the Cartesian product of sequences.

    Arguments:
        sequence (list): Sequences to compute the product of

    Returns:
        A list of tuples
    """

    if not sequence:
        return iter(((),))
    return (items + (item,)
            for items in nd_product(sequence[:-1]) for item in sequence[-1])

