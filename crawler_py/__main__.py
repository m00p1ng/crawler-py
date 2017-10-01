import sys
import os.path

PATH = os.path.realpath(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(PATH)))

import crawler_py

if __name__ == '__main__':
    try:
        crawler_py.main()
    except KeyboardInterrupt:
        print("\n<-- bye ja -->")
