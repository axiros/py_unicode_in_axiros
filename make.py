#!/usr/bin/env python
from time import sleep
import os

if __name__ == '__main__':
    oldstat = 0
    print 'looping, checking changes of show.markdown'
    while True:
        stat = os.stat('./show.markdown')
        if stat == oldstat:
            sleep(1)
            continue
        oldstat = stat
        os.system('pandoc show.markdown -o show.html -s -V "theme:black" -t revealjs')
        t = open('./reveal.js/index.html.tmpl').read()
        s = open('./show.html').read()
        title = s.split('<title>', 1)[1].split('</title')[0]
        body = s.split('<body>', 1)[1].split('<script ')[0]
        t = t.replace('_TITLE_', title).replace('_CONTENT_', body)
        open('./reveal.js/index.html', 'w').write(t)
        os.system('cd ./reveal.js')
        print 'open ./reveal.js/index.html'


