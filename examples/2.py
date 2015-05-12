#!/usr/bin/env python
u1 = open('j1').read().decode('utf-8')
u2 = open('j2').read().decode('utf-8')
print u1, u2, isinstance(u1, unicode)
print u1 == u2

