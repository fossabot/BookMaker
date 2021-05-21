"""Python package using PEP 517 hooks
"""

import os
import subprocess

from .about import VERSION as __version__

class my_class():
    def main(self):
        prefix = os.path.dirname(os.path.realpath(__file__))
        python = os.path.join(prefix, 'venv/bin/python')
        module = os.path.join(prefix, 'BookMaker.py')
        completed = subprocess.run([python, module])
        # print('returncode:', completed.returncode)

def main():
    instance = my_class()
    instance.main()

# Run if called directly
if __name__ == '__main__':
    main()
