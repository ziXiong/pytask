# -*- coding: utf-8 -*-


from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import UniqueConstraint

Model = declarative_base()


class Task(Model):
    """
    Task model for saving task info.
    """

    __tablename__ = 't_task'

    id = Column(Integer, primary_key=True, autoincrement=True)
    biz_code = Column(String(50), nullable=False)  # Business code
    biz_num = Column(String(100), nullable=False)  # Code that identify each task
    when = Column(DateTime, nullable=False, index=True)  # When to execute task
    biz_ext = Column(Text)  # Addition data for executing task

    status = Column(Boolean, nullable=False, server_default='0')
    version = Column(SmallInteger, nullable=False, server_default='0')
    create_time = Column(DateTime, nullable=False)
    update_time = Column(DateTime, nullable=False)

    __table_args__ = (UniqueConstraint('biz_num', 'biz_code', name='idx_task_biz'))

    def __str__(self):
        return 'biz_code: %s, biz_num: %s, when: %s, biz_ext: %s' % \
               (self.biz_code, self.biz_num, self.when, self.biz_ext)


class TaskException(Exception):
    pass


class TaskHandler:
    def handle(self, task):
        """
        子类必需重写此方法处理业务逻辑
        :param task:
        :return:
        """
        raise TaskException('must ovrride process')

    def get_biz_code(self):
        """
        子类返回业务场景编码
        :return:
        """
        raise TaskException('must override get_biz_code')
