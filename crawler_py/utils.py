''' utilities module '''

import os
from datetime import datetime
from termcolor import colored

from .settings import EXTRACT_EXTENSIONS


def print_log(message, color='white'):
    ''' Print log message with timestamp '''

    timestamp = datetime.now().strftime('%d-%m-%yT%H:%M:%S.%f')[:-3]
    print(colored(f"[{timestamp}]  {message}", color))


def check_extension(filename):
    '''
    Check extentions that can extract

    Parameter:
        filename (string): filename that need check
    Return:
        (bool): if in EXTRACT_EXTENSIONS return True
    '''
    extension = os.path.splitext(filename)[1]
    if extension in EXTRACT_EXTENSIONS or extension is '':
        return True
    return False
