'''
Command line tool to execute jobs in Cirrus CI
'''

from .logging import setup
from .api import CirrusAPI

log = setup()
del setup
