# -*- coding: utf-8 -*-
"""
this example demonstrated how to init the pytask db. Only need to be executed once.
"""

import pytask

# config dict, like you config your SQLAlchemy db.
sqlchemy_db = dict(
    drivername='mysql+mysqlconnector',
    host='localhost',
    username='username',
    password='password',
    database='mydatabase',
)

pytask.config(sqlchemy_db)

# do this, then you can see a table `t_task` in your database.
pytask.init_db()


