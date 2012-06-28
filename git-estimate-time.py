from git import *
import pprint
import os

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

seconds_before_commit = 30 * 60

repo = Repo(os.getcwd())
assert repo.bare == False

head = repo.head.reference

start_hex = "81c77d116cf417fa91c55b31db5ee176116bf08b"
end_hex = "ddd73378bbb32ee26fd871df404f05cf361ef821"

relevant_log_entries = get_relevant_entries(head.log(), start_hex, end_hex)

pprint.pprint(get_work_time(relevant_log_entries, seconds_before_commit))

assert len(relevant_log_entries) > 0

