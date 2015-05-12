#!/usr/bin/env python
import sys
from json import dumps, loads

here  = sys.argv[1]
there = loads(dumps(here))
print here, there
print here == there

