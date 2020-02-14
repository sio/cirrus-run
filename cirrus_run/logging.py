'''
Logging setup
'''

import logging
import os


class ShyLogHandler(logging.StreamHandler):
    '''Emit messages only if root logger has no other handlers'''
    root = logging.getLogger()
    def emit(self, record):
        if not self.root.hasHandlers():
            super().emit(record)


def setup():
    package = __name__.split('.')[0]
    log = logging.getLogger(package)
    if getattr(log, 'initialized', False):
        return log

    log_file = os.environ.get('CIRRUS_LOG_FILE')
    log_stdout = True

    log.level = logging.WARNING

    if log_file:
        handler = logging.FileHandler(log_file, encoding='utf-8')
        handler.level = logging.DEBUG
        handler.formatter = logging.Formatter('%(asctime)s - %(message)s')
        log.addHandler(handler)

    if log_stdout:
        handler = ShyLogHandler()
        handler.level = logging.DEBUG
        log.addHandler(handler)

    log.initialized = True
    return log
