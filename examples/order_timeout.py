# -*- coding: utf-8 -*-
"""
This example demonstrated how to register an handler and add a task and that is all you need to do to run a task.
"""

import json
from datetime import datetime, timedelta

import pytask
from pytask import Task

# First Step: config pytask db
sqlchemy_db = dict(
    drivername='mysql+mysqlconnector',
    host='localhost',
    username='username',
    password='password',
    database='mydatabase',
)
pytask.config(sqlchemy_db)


# Second Step: register a task handler
class OrderTimeoutHandler(pytask.TaskHandler):
    def handle(self, task):
        data = json.loads(task.biz_ext)
        ### do the timing task ###
        # order = get_order_by_id(data['id'])
        # order.set_timeout(True)

    def get_biz_code(self):
        return 'order_timeout'  # this code identify a task

pytask.register_handler(OrderTimeoutHandler)


# Third Step: add an task
timeout_time = datetime.now() + timedelta(minutes=30)
data = dict(id=1)  # whatever data you need when calling handler.
pytask.add_task(Task(biz_code='order_timeout', when=timeout_time, biz_ext=json.dumps(data)))


# Fourth Step: start pytask. pytask will run in another thread.
pytask.start(daemon=False)
