# -*- coding: utf-8 -*-

import logging

from datetime import datetime
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine

from .models import Task, Model
from .config import settings

logger = logging.getLogger(__name__)


class TaskStore:

    @property
    def session(self):
        if not hasattr(self, '_session'):
            engine = create_engine("%s?charset=utf8mb4" % URL(**settings.sqlachemy_db), pool_recycle=3600)
            self._session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        return self._session

    def add_task(self, task):
        """insert task to db"""
        assert isinstance(task, Task), 'add task only accept Task instance, type %s got' % type(task)

        now = datetime.now()
        task.create_time = now
        task.update_time = now
        task.status = 0

        self.session.add(task)
        self.session.commit()

        return task.id

    def finished_task(self, biz_code, biz_num):
        """delete task from db"""
        self.session.query(Task).filter(Task.biz_code == biz_code, Task.biz_num == biz_num).delete()
        self.session.commit()

    def get_undo_tasks(self):
        """get undo task from now"""
        now = datetime.now()
        undo_tasks = self.session.query(Task).filter(Task.status == 0, Task.when <= now).order_by(
            Task.when).limit(settings.batch_undo_rows).all()

        processing_tasks = []
        for task in undo_tasks:
            # Optimistic Lock
            rows = self.session.query(Task).filter(Task.id == task.id, Task.status == 0).update(
                {Task.status: 1, Task.version: Task.version + 1, Task.update_time: datetime.now()})
            if rows == 1:
                processing_tasks.append(task)
        self.session.commit()
        return processing_tasks

    def retry_task(self, biz_code, biz_num, next_time):
        """set when to a retry task"""
        self.session.query(Task).filter(Task.biz_code == biz_code, Task.biz_num == biz_num).update(
            {Task.status: 0, Task.when: next_time, Task.update_time: datetime.now()})
        self.session.commit()

    def init_db(self):
        Model.metadata.create_all(self.session.session_factory.kw['bind'])


store_engine = TaskStore()
