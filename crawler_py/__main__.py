import sys
import os.path

path = os.path.realpath(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

import crawler_py

if __name__ == '__main__':
    crawler_py.main()