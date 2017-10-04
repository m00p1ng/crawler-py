''' utilities module '''
import os
import math
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
    extension = os.path.splitext(filename)[1].lower()
    if extension in EXTRACT_EXTENSIONS or extension == '':
        return True

def convert_size(size):
    if size == 0:
        return "0 B"
    name = ("B", "KB", "MB")
    i = int(math.floor(math.log(size, 1024)))
    p = math.pow(1024, i)
    s = round(size / p, 2)
    return f"{s} {name[i]}"
