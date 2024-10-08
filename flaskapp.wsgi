#!/usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/home/ubuntu/flaskapp")

from flaskapp import app as application
