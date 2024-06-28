import win32api,win32process,win32con
from logtail import LogtailHandler
import logging
    
def GetMeLogger(log_token):
    handler = LogtailHandler(log_token)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.handlers = []
    logger.addHandler(handler)

    return logger

def setup_strat(log_token):
    set_realtime_priority()

    return GetMeLogger(log_token)

def set_realtime_priority():
    pid = win32api.GetCurrentProcessId()
    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
    win32process.SetPriorityClass(handle, win32process.REALTIME_PRIORITY_CLASS)