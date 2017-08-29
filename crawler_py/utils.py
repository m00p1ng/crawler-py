''' utilities module '''
from datetime import datetime
from termcolor import colored


def print_log(message, color='white'):
    ''' Print log message with timestamp '''

    timestamp = datetime.now().strftime('%d-%m-%yT%H:%M:%S.%f')[:-3]
    print(colored(f"[{timestamp}]  {message}", color))
