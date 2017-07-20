
# Problem 3
# ---------
# Returns a representation of the information in default_db and update_db
#  This representation will be used to implement the other methods
def build_rep(default_db, update_db):
    meetings = {}  # subj => list of (week, day, time)

    # start by processing default schedule to create complete
    # of meetings for each class
    for subj,time,day in default_db:
        mlist = meetings.get(subj,[])
        meetings[subj] = mlist  # in case mlist is brand new
        for week in range(1,16):
            mlist.append((str(week),day,time))

    # now process updates
    for action,subj,time,day,week in update_db:
        # get list of meetings for this subj
        mlist = meetings.get(subj,[])
        meetings[subj] = mlist  # in case mlist is brand new
        # process udpate
        if action == 'DELETE':
            mlist.remove((week,day,time))
        elif action == 'ADD':
            mlist.append((week,day,time))

    return meetings

# Returns a list of lists class_dates where class_dates[i] is a list of all
#  dates on which class_list[i] meets
def get_class_days(class_list, rep):
    result = [[(week,day) for week,day,time in rep.get(subj,[])]
              for subj in class_list]
    return result

# Returns a list of all classes that never meet before the specified time
def get_late_classes(time, rep):
    # return True if there's no meeting time on mlist
    # that's before xtime
    def never_meet_before(mlist,xtime):
        xtime = int(xtime)
        for week,day,time in mlist:
            if int(time) < xtime:
                return False
        return True

    return [subj
            for subj in rep
            if never_meet_before(rep[subj],time)]
