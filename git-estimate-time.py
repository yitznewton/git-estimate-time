#!/usr/bin/python

from os import getcwd, popen
import sys
import re
from pprint import pprint

def get_relevant_entries(start_hex, end_hex):
    should_use = False
    is_at_end = False
    entries = []

    command = 'git log --reverse --format=format:"%H\t%ae\t%at"'
    git_log_output = popen(command)

    while 1:
        line = git_log_output.readline()

        if not line:
            break

        pattern = re.compile("^([0-9a-f]+)\t([^\t]+)\t([\d]+)$")
        matches = pattern.match(line.strip())
        
        if matches.group(1) == start_hex:
            should_use = True

        if should_use:
            entries.append(matches.groups())

        if matches.group(1) == end_hex:
            is_at_end = True
            break

    if not is_at_end:
        return []

    return entries

def get_work_time(entries, seconds_before_commit):
    commits = get_user_commit_times(entries, seconds_before_commit)
    total_times = {}

    for user, times in commits.iteritems():
        for i, item in enumerate(times):
            if i == 0:
                total_times[user] = seconds_before_commit
                continue

            since_last = int(times[i]) - int(times[i-1])

            if since_last < seconds_before_commit:
                total_times[user] += since_last
            else:
                total_times[user] += seconds_before_commit

    return total_times

def get_user_commit_times(entries, seconds_before_commit):
    commits_by_user = {}

    for item in entries:
        name = item[1]
        time = item[2]

        if name not in commits_by_user:
            commits_by_user[name] = []

        commits_by_user[name].append(time)

    return commits_by_user

if len(sys.argv) != 4:
    print "Usage: git-estimate-time.py start_hex end_hex seconds_before_commit"
    exit(1)

assert re.compile("\d+").match(sys.argv[3])

seconds_before_commit = int(sys.argv[3])

relevant_log_entries = get_relevant_entries(sys.argv[1], sys.argv[2])

assert len(relevant_log_entries) > 0

work_time = get_work_time(relevant_log_entries, seconds_before_commit)

for name, time in work_time.iteritems():
    print ""
    print name + ": " + str(time) + " seconds"
    print name + ": " + str(float(time) / 60) + " minutes"
    print name + ": " + str(float(time) / 60 / 60) + " hours"

