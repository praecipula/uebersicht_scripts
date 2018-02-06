#!/usr/bin/env python

import asana
import json
import traceback
import datetime
import dateutil.parser
from os import path

__output = None
def output():
    global __output
    if not __output:
        __output = {
                'errors':[],
                'results':{}
        }
    return __output

class MyTasks(object):

    ATM_ID=153678405088708

    def __init__(self):
        mydir = path.dirname(__file__)
        secrets_path = path.join(mydir, "secrets.json")
        secrets = json.load(open(secrets_path))
        self._client = asana.Client.access_token(secrets['asana_personal_access_token'])
        self._memoized_tasks = None
        
    def me(self):
        me = self._client.users.me()
        user = {}
        user['name'] = me["name"]
        user['pic'] = me["photo"]["image_21x21"]
        return user

    def memoized_tasks(self):
        # We have 2 approaches here:
        # tasks?assignee=me and /projects/[ATM_ID]
        # Since the second one would preserve iteration order from my ATM fairly closely, let's go with that.
        if not self._memoized_tasks:
            self._memoized_tasks = [task for task in self._client.tasks.find_all(project=MyTasks.ATM_ID,
                completed_since="now",
                fields=["name", "due_on", "due_at"]
                )]
        return self._memoized_tasks

    # Define tasks due "soon" as from one week ago to one week hence, in order
    def tasks_due_soon(self):
        nowish = datetime.datetime.now()
        last_week = nowish - datetime.timedelta(7)
        next_week = nowish + datetime.timedelta(7)
        task_set = []
        for task in self.memoized_tasks():
            in_set = False
            due = None
            if task["due_at"]:
                due = dateutil.parser.parse(task["due_at"])
                if due > last_week and due < next_week:
                    in_set = True
            if task["due_on"]:
                due = dateutil.parser.parse(task["due_on"])
                if due > last_week and due < next_week:
                    in_set = True
            if in_set:
                record = {}
                record["task"] = task
                record["due"] = due
                task_set.append(record)
        return [record["task"] for record in sorted(task_set, key=lambda record: record["due"], reverse=True)][0:5]

    def stale_tasks(self):
        pass


if __name__ == "__main__":
    try:
        mt = MyTasks()
        output()['results']['user'] = mt.me()
        output()['results']['total_assigned_tasks'] = len(mt.memoized_tasks())
        output()['results']['focus'] = mt.tasks_due_soon()
        print json.dumps(output())
    except Exception as e:
        output()['errors'].append(traceback.format_exc())
        print json.dumps(output())
