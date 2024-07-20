#!c:\users\abi\abigitprojects\code-complexity-analyzer\venv\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'complexity==0.9.1','console_scripts','complexity'
__requires__ = 'complexity==0.9.1'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('complexity==0.9.1', 'console_scripts', 'complexity')()
    )
