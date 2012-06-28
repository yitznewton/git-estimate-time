#!/usr/bin/python

from git import *
from os import getcwd
import sys
import re

def get_relevant_entries(log, start_hex, end_hex):
    should_use = False
    entries = []

    for item in log:
        current_hex = item[1]
        if current_hex == start_hex:
            should_use = True

        if should_use:
            entries.append(item)

        if current_hex == end_hex:
            break

    return entries

def get_work_time(entries, seconds_before_commit):
    commits = get_user_commit_times(entries, seconds_before_commit)
    total_times = {}

    for user, times in commits.iteritems():
        for i, item in enumerate(times):
            if i == 0:
                total_times[user] = seconds_before_commit
                continue

            since_last = times[i] - times[i-1]

            if since_last < seconds_before_commit:
                total_times[user] += since_last
            else:
                total_times[user] += seconds_before_commit

    return total_times

def get_user_commit_times(entries, seconds_before_commit):
    commits_by_user = {}

    for item in entries:
        name = item[2].name
        time = item[3][0] + item[3][1]

        if name not in commits_by_user:
            commits_by_user[name] = []

        commits_by_user[name].append(time)

    return commits_by_user

if len(sys.argv) != 4:
    print "Usage: git-estimate-time.py start_hex end_hex seconds_before_commit"
    exit(1)

assert re.compile("\d+").match(sys.argv[3])

seconds_before_commit = int(sys.argv[3])

repo = Repo(getcwd())
assert repo.bare == False

head = repo.head.reference

relevant_log_entries = get_relevant_entries(head.log(), sys.argv[1], sys.argv[2])

assert len(relevant_log_entries) > 0

work_time = get_work_time(relevant_log_entries, seconds_before_commit)

for name, time in work_time.iteritems():
    print ""
    print name + ": " + str(time) + " seconds"
    print name + ": " + str(float(time) / 60) + " minutes"
    print name + ": " + str(float(time) / 60 / 60) + " hours"

