# -*- coding: utf-8 -*-

from .executor import register_handler, send_shutdown_signal, run
from .store import store_engine
from .models import Task, TaskHandler
from .config import config


def add_task(task):
    """
    添加新任务
    :param task:
    :return:
    """
    store_engine.add_task(task)


def cancel_task(biz_code, biz_num):
    """
    取消未执行的任务
    :param biz_code: 任务执行处理器编码
    :param biz_num: 任务编码
    :return:
    """
    store_engine.finished_task(biz_code, biz_num)


def register_task_handler(task_handler):
    """
    注册任务处理器
    :param task_handler: 任务处理器
    :return:
    """
    register_handler(task_handler)


def start():
    """
    开启服务
    :return:
    """
    run()


def shutdown():
    """
    关闭服务
    :return:
    """
    send_shutdown_signal()
