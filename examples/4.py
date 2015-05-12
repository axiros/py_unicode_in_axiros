#!/usr/bin/env python
import sys
from json import dumps, loads

print loads(dumps(sys.argv[1]))
print 'success'

