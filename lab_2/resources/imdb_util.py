#!/usr/bin/env python2.7

# This file contains helpers methods that were used to generate the .json files for Lab #2
# You need not read, use, or modify this file

import sqlite3
import datetime
import os, sys, json

conn = sqlite3.connect('db/movies_large.db')
conn_small = sqlite3.connect('db/movies_small.db')

def dump_small_data_set():
    with open('small.json', 'w') as f:
        json.dump(get_small_data_set(), f)

def dump_large_data_set():
    with open('large.json', 'w') as f:
        json.dump(get_large_data_set(), f)

# Retrieves a very large list of triplets [Actor 1 id, Actor 2 id, Movie id], where "Actor 1 id"
# and "Actor 2 id" acted in "Movie name id" together.
def get_large_data_set():
    return get_data_set(False)


# Retrieves a small list of triplets [Actor 1 id, Actor 2 id, Movie id], where "Actor 1 id"
# and "Actor 2 id" acted in "Movie name id" together.
def get_small_data_set():
    return get_data_set(True)


def get_data_set(small, verbose=False):
    if verbose:
        print "Retrieving the data set",
    begin = datetime.datetime.now()
    if verbose:
        print "Starting time", begin

    try:
        command = "select distinct t1.actor_id, t2.actor_id, t3.tmdb_id from acted_at t1 inner join acted_at t2 on t1.movie_id = t2.movie_id join movies t3 on t2.movie_id = t3.tmdb_id;"
        if small:
            data = conn_small.execute(command).fetchall()
        else:
            data = conn.execute(command).fetchall()
        end = datetime.datetime.now()
        if verbose:
            print "Done at ", end
            print "Total time - ", (end - begin).total_seconds()
        return data
    except sqlite3.Error as e:
        print e.args[0]


# Retrieves a list of actors from the Database
def get_actors():
    print "Retrieving the data set",
    begin = datetime.datetime.now()
    print "Starting time", begin

    list_of_triplets = []
    try:
        command = "select distinct actors.tmdb_id, actors.name from actors"
        for row in conn_small.execute(command).fetchall():
            list_of_triplets += [(row[0], row[1])]
        end = datetime.datetime.now()
        print "Done at ", end
        print "Total time - ", (end - begin).total_seconds()
        return list_of_triplets
    except sqlite3.Error as e:
        print e.args[0]


# Retrieves actor name by its id
def get_actor_name_by_id(actor_id):
    try:
        command = "select name from actors t where t.tmdb_id = ?;"
        return conn.execute(command, (actor_id,)).fetchone()[0]
    except sqlite3.Error as e:
        print e.args[0]

# Retrieves movie name by its id
def get_movie_name_by_id(movie_id):
    try:
        command = "select name from actors t where t.tmdb_id = ?;"
        return conn.execute(command, (movie_id,)).fetchone()[0]
    except sqlite3.Error as e:
        print e.args[0]

# For test purposes - Verifies if a path is valid
def is_path_valid(data, path):
    if path is not None:
        if len(path) <= 0:
            return True
    for i in xrange(0,len(path)-1):
        if path[i + 1] not in data[path[i]]:
            return False
    return True

if __name__ == "__main__":
    dump_small_data_set()
    dump_large_data_set()
