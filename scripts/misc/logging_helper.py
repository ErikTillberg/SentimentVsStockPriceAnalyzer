import logging
import os
import errno
import time
import sys

from . import color_stream_handler

def setup_logging(log_name):
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    #
    _make_sure_path_exists('logs')
    #
    stream_handler = color_stream_handler.ColorStreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(levelname)-6s : %(name)-25s : %(message)s'))
    file_log_handler = logging.FileHandler('logs/%s - %s.log'%(log_name, time.strftime("%a, %d %b %Y %Hh%Mm%Ss",time.localtime())))
    file_log_handler.setFormatter(logging.Formatter('%(levelname)-6s : %(name)-25s : %(message)s'))
    #
    root_logger.addHandler(stream_handler)
    root_logger.addHandler(file_log_handler)
    #
    logger = logging.getLogger(__name__)
    #
    ##############
    #
    _install_thread_excepthook()
    sys.excepthook = _ExceptionLogger().handle_exception

def _make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

class _ExceptionLogger(object):
    def __init__(self):
        self._logger = logging.getLogger(__name__)
    #
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        # see here: http://stackoverflow.com/a/16993115/3731982
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        #
        self._logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    #

def _install_thread_excepthook():
    '''
    Workaround for sys.excepthook thread bug
    From http://spyced.blogspot.com/2007/06/workaround-for-sysexcepthook-bug.html (https://sourceforge.net/tracker/?func=detail&atid=105470&aid=1230540&group_id=5470).
    Call once from __main__ before creating any threads.
    If using psyco, call psyco.cannotcompile(threading.Thread.run)
    since this replaces a new-style class method.
    '''
    import threading
    init_old = threading.Thread.__init__
    def init(self, *args, **kwargs):
        init_old(self, *args, **kwargs)
        run_old = self.run
        def run_with_except_hook(*args, **kw):
            try:
                run_old(*args, **kw)
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                sys.excepthook(*sys.exc_info())
        self.run = run_with_except_hook
    threading.Thread.__init__ = init