"""Python package using PEP 517 hooks
"""
__import__("pkg_resources").declare_namespace(__name__)

__version__ = '0.24b2'

import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
__package__ = 'bookmaker'
print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__, __name__, str(__package__)))
from .BookMaker import main as BM_main


class my_class():
    def main(self):
        print(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'venv/bin/python'))
        os.environ['PYTHONHOME'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'venv/bin/python')

        BM_main()


def main():
    instance = my_class()
    instance.main()


# Run if called directly
if __name__ == '__main__':
    main()
