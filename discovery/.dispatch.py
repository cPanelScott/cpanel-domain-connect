#!/bin/python

from os.path import dirname, abspath, join
import sys

# Find code directory relative to our directory
THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, 'lib'))
sys.path.append(CODE_DIR)
sys.path.append('/usr/local/cpanel/3rdparty/python/2.7/lib/python2.7/site-packages')

from wsgiref.handlers import CGIHandler
from Domainconnect import app

CGIHandler().run(app)
