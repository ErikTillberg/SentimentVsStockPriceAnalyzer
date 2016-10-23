from __future__ import print_function
import requests
import logging
#
def get_sentiment_from_text(text, apikey):
    data = {
        'txt': text
    }
    headers = {
        "X-Mashape-Key": apikey,
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    r = requests.post('https://community-sentiment.p.mashape.com/text/', headers=headers, data=data)
    #
    return r.json()
    '''
    Example response:

    {
        "result": {
            "confidence": "96.7434",
            "sentiment": "Positive"
        }
}
    '''
#
class ExceptionLogger(object):
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
#
if __name__=='__main__':
    import sys
    _install_thread_excepthook()
    sys.excepthook = ExceptionLogger().handle_exception
    #
    ##############
    #
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    #
    import color_stream_handler
    stream_handler = color_stream_handler.ColorStreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(levelname)-6s : %(name)-25s : %(message)s'))
    #file_log_handler = logging.FileHandler('alchemy.log')
    #
    root_logger.addHandler(stream_handler)
    #root_logger.addHandler(file_log_handler)
    #
    logger = logging.getLogger(__name__)
    #
    ##############
    #
    import yaml
    with open('api_keys.yaml', 'r') as f:
        api_keys = yaml.load(f)
    #
    apikey = api_keys['marketplace']['apikey']
    #
    ##############
    #
    print(get_sentiment_from_text('Today is a good day', apikey))
    print(get_sentiment_from_text('Today is a bad day', apikey))
    #
    '''
    import time
    start = time.clock()
    for x in xrange(100):
        get_sentiment_from_text('Today is a bad day', apikey)
    print(time.clock()-start)
    '''
#
