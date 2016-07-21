# -*- coding: utf-8 -*-


class ConfigObject:
    """config object for pytask"""

    def __getattr__(self, item):
        raise Exception('pytask is not properly configured, losing %s' % item)

settings = ConfigObject()


def config(sqlachemy_url, second_of_wait_task=10, batch_undo_rows=20):
    """
    config pytask
    :param sqlachemy_url: sqlachemy_url to connect db.
    :param second_of_wait_task: interval between pytask to check if there is undo task.
    :param batch_undo_rows: max num of tasks to be executed each time.
    """
    settings.sqlachemy_url = sqlachemy_url
    settings.second_of_wait_task = second_of_wait_task
    settings.batch_undo_rows = batch_undo_rows
