"""Python package using PEP 517 hooks
"""

import sys
import os
import subprocess
from pathlib import Path # if you haven't already done so

file = Path(__file__).resolve()
try:
    sys.path.append(str(file.parents[1]))
    print(f'Allow the import to look in {str(file.parents[1])}')
    from src.bookmaker.about import VERSION as __version__
except ModuleNotFoundError:
    sys.path.append(str(file.parents[2]))
    print(f'Failed; it needs to look in {str(file.parents[2])}')
    from bookmaker.about import VERSION as __version__

class my_class():
    def main(self):
        prefix = os.path.dirname(os.path.realpath(__file__))
        python = os.path.join(prefix, 'venv/bin/python')
        module = os.path.join(prefix, 'BookMaker.py')
        print(f'Running subprocess {python} {module}')
        completed = subprocess.run([python, module])
        # print('returncode:', completed.returncode)

def main():
    instance = my_class()
    instance.main()

# Run if called directly
if __name__ == '__main__':
    main()
