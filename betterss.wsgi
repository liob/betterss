import os, sys
cwd = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, cwd)
from betterss import app as application
