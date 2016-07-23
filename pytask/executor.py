# -*- coding: utf-8 -*-

import time
import logging
import threading

from .config import settings
from .store import store_engine

logger = logging.getLogger(__name__)
# 任务处理器
handler_map = {}
# 结束任务信号通道
shutdown_signal = False
is_running = False


def register_handler(task_handler):
    handler_map[task_handler.get_biz_code()] = task_handler
    logger.info('Register task handler %s' % task_handler.get_biz_code())


def send_shutdown_signal():
    global shutdown_signal, is_running
    shutdown_signal = True
    is_running = False


class TaskProcessThread(threading.Thread):

    def run(self):
        logger.info('start the task processor.....')
        global is_running
        is_running = True
        while not shutdown_signal:
            undo_tasks = store_engine.get_undo_tasks()
            logger.debug('get undo task size: %s' % len(undo_tasks))

            if not undo_tasks:
                time.sleep(settings.second_of_wait_task)
                continue

            for task in undo_tasks:
                try:
                    logger.info('begin process the task: %s' % task)
                    next_time = handler_map.get(task.biz_code).handle(task)
                    if next_time:
                        logger.info('retry the task: %s' % task)
                        store_engine.retry_task(task.id, next_time=next_time)
                    else:
                        logger.info('finished the task: %s' % task)
                        store_engine.finished_task(task.id)
                except Exception:
                    logger.exception('fail process task: %s' % task)
        else:
            logger.info('the task executor had shutdown')


def run(daemon):
    if not is_running:
        TaskProcessThread(daemon=daemon).start()
    else:
        logger.info('task is running, not allow start again')
