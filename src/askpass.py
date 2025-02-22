#!/usr/bin/env python
#
# Short & sweet script for use with git clone and fetch credentials.
# Requires GIT_USERNAME and GIT_PASSWORD environment variables,
# intended to be called by Git via GIT_ASKPASS.
#

from sys import argv
from os import environ

if argv[1].startswith("Username"):
    print (environ['GIT_USERNAME'])
    exit()

if argv[1].startswith("Password"):
    print (environ['GIT_PASSWORD'])
    exit()

exit(1)
