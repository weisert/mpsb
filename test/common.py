import sys
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
_SRC = os.path.join(_ROOT, 'src')
TESTS = os.path.join(_ROOT, 'test')

sys.path.append(os.path.join(_SRC, 'scripts'))
