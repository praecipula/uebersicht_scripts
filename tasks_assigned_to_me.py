#!/usr/bin/env python

import asana
import json
import traceback
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

    def __init__(self):
        mydir = path.dirname(__file__)
        secrets_path = path.join(mydir, "secrets.json")
        secrets = json.load(open(secrets_path))
        self._client = asana.Client.access_token(secrets['asana_personal_access_token'])
        
    def me(self):
        me = self._client.users.me()
        output()['results']['user'] = {}
        output()['results']['user']['name'] = me["name"]
        output()['results']['user']['pic'] = me["photo"]["image_21x21"]

    def tasks_due_today(self):
        pass

    def stale_tasks(self):
        pass


if __name__ == "__main__":
    try:
        mt = MyTasks()
        mt.me()
        mt.tasks_due_today()
        print json.dumps(output())
    except Exception as e:
        output()['errors'].append(traceback.format_exc())
        print json.dumps(output())
