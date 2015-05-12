# Text In Axiros Python Processes

## Axiros GmbH
May, 2015, Gunther Klessinger

<br>
<br>
<br>
<br>
Themes:
[white](?theme=white)
[black](?theme=black) 
[beige](?theme=beige) 
[moon](?theme=moon)
[league](?theme=league)
[night](?theme=night)
[serif](?theme=serif)
[simple](?theme=simple)
[sky](?theme=sky)
[solarized](?theme=solarized) 

- ``Esc`` to get an overview
- ``s`` to present

# Whats the Problem, Why Should I Care

## what you see != what you get

    #!/usr/bin/env python
    s1 = open('j1').read()
    s2 = open('j2').read()
    print s1, s2
    print s1 == s2

    $ ./1.py
    José José
    False

. . .

False !?


## unicode to the rescue?

    #!/usr/bin/env python
    u1 = open('j1').read().encode('utf-8')
    u2 = open('j2').read().encode('utf-8')
    print u1, u2, isinstance(u1, unicode)
    print u1 == u2

    $ ./2.py
    José José True
    False

same, same...

## foreground ok - logfile crashes

    #!/usr/bin/env python
    u1 = open('j1').read().decode('utf-8')
    print u1
    print 'success'

    $ ./3.py
    José
    success

    $ ./3.py > test
    UnicodeEncodeError: 'ascii' codec can't encode character u'\xe9' in position 3:
    ordinal not in range(128)

. . .

missing: "``success``"

## no prob

"I never use ``decode``, don't even know what it does"

But: json you DO use!


    #!/usr/bin/env python
    import sys
    from json import dumps, loads
    print loads(dumps(sys.argv[1]))
    print 'success'

run:

    $ ./4.py Hans | more
    Hans
    $ ./4.py José | more
    Traceback (most recent call last):
        print loads(dumps(sys.argv[1]))
    UnicodeEncodeError: 'ascii' codec can't encode character...


## apropos: json

    #!/usr/bin/env python
    import sys
    from json import dumps, loads

    here  = sys.argv[1]
    there = loads(dumps(here))
    print here, there
    print here == there

. . .

    $ ./5.py Hans
    Hans Hans
    True
    $ ./5.py José
    José José
    False
    $ ./5.py José | more
    Traceback (most recent call last):
    UnicodeEncodeError: 'ascii' codec can't encode character u'\xe9' in
    position 3: ordinal not in range(128)
    José


## not to forget

the well known ``str()``, ``%s`` problems

    >>> from json import loads, dumps
    >>> received = loads(dumps('José'))
    >>> str(received)
    Traceback (most recent call last):
    UnicodeEncodeError: 'ascii' codec cant encode character
    u'\xe9' in position 3:
    ordinal not in range(128)

. . .

    >>> json.loads(json.dumps('Hans')) + 'José'
    Traceback (most recent call last):
    UnicodeEncodeError: 'ascii' codec cant encode character...

. . .

    >>> u'%s' % 'José'
    Traceback (most recent call last): ...
    UnicodeDecodeError: 'ascii' codec cant decode ...

-----------

# Doomed!?

## Check Google

Python 2 unicode handling is

- [broken](https://news.ycombinator.com/item?id=7012683)
- [pain](http://nedbatchelder.com/text/unipain.html)
- [inconsistent, frustrating](https://pythonhosted.org/kitchen/unicode-frustrations.html)
- [extremly shitty](http://t-a-w.blogspot.de/2013/09/python-3-unicode-apparently-no-longer.html)
- [possibly leading to data
  corruption](http://python-notes.curiousefficiency.org/en/latest/python3/text_file_processing.html)
- [causing nervous breakdowns](https://github.com/thp/python2sucks)

and 10000 of the like, typically pointing to Python3's unicode everywhere
model.

Which is the
[major](http://pyvideo.org/video/289/pycon-2010--mastering-python-3-i-o) compatibility breaker between 2 and 3.

# Answers

## The official way

Decode [everywhere](http://nedbatchelder.com/text/unipain.html) - like in Py3

<img src="../images/sandwich.png" alt="sw" style="width: 450px;" />


## Feasible

Think a second about what this means:

- **Humans** process text, expressed in *symbols* - which the unicode standard enumerates
  ongoingly into currently around 1Mio codepoints
- **Systems** process, forward, store only bytes
- **[Standards](http://www.ietf.org/download/rfc-index.txt)** define how systems
  interact - unicode is next to irrelevant here, an [example](http://carl.sandiego.edu/bus188/osi_model.htm)
for layer6 in the OSI model.

## Standards Vs. Unicode

Any text identifier in any standard is: **ASCII**.

In any protocol. By *definition* of being a global standard.

Should we now convert ANY text from outside the process?

    for k, v in my_payload.items():
        if isinstance(v, basestring):
            my_payload[k] = v.decode('utf-8') # is it utf-8?! Nesting?


For getting 'advantages' like this:

    >>> RAM, unic = sys.getsizeof, u' ' * 100000
    >>> round(float(RAM(unic)) / RAM(str(unic)), 2)
    4.0


## Irrelevancy of Unicode

The theory and idea behind having standards accepted, ratified, and agreed upon
by nations around the world, is to ensure that the system from country A will
be easily integrated with the system from country B with little effort.


"*While unicode maps the BIGGEST POSSIBLE set of meaningful information for inter
HUMAN communication, standards define the smallest necessary one for inter SYSTEMS
communication.*"

# Axiros Way

## Bytestring Sandwich

- All text is str() type.
- Unicode only as a function
- Like Go, Rust, other modern languages built for inter systems communication

## Which functions?

- Counting number of symbols (but mind
  [normalization](https://dev.twitter.com/overview/api/counting-characters))
- upper()
- looping over symbols

unicode knows about the 'meaning' of characters for humans:

    >>> s = 'José'; print '%s %s' % (s.upper(),unicode(s).upper())
    JOSé JOSÉ
    >>> for c in s: print c,
    J o s ? ?
    >>> for c in unicode(s): print c
    J o s é


## defaultencoding

    >>> print '%s %s' % (s.upper(),unicode(s).upper())

No encode, decode - why did this not break, two times?

Python's does **implicit** type conversions for us - if we [configure it
right](http://www.ianbicking.org/illusive-setdefaultencoding.html):

At process setup time (e.g. paster):

    if __name__ == '__main__':
        import sys; reload(sys); sys.setdefaultencoding('utf-8')

. . .

And in packages' __init__, to enforce this:

    if 'ascii' in sys.getdefaultencoding().lower():
        raise Exception(("sys.defaultencoding not set! "
            "Axiros modules rely on full range implicit encoding!"))




## Json

json restricted itself to transferring human symbols only.

Why?
This de-facto standard came from the human text processing world (origins of
JS).

We [convert](https://github.com/axiros/nested_encode) any json right after loads:

    >>> from nested_encode import encode_nested # ty, Stephan
    >>> encode_nested(json.loads(data))

Any other Py2 library we use anyway delivers byte strings as default (e.g. redis).

# Perfect World

## All works

    s = 'é'; open('f', 'w').write(s)
    os.stat('f').st_size == len(s) # True
    unicode(str(u'é'))             # works
    print u'José'                  # can be piped w/o crash
    s == unicode(s)                # True

Only take for bytes without a meaning
(i.e. the MS codepages
[fubar](https://github.com/AXGKl/unicode-kills-python3#bytes-without-a-meaning-the-ibmmicrosoft-codepage-fubar---and-its-relevance-today))


## Links


- [This](https://github.com/axiros/unicode_in_axiros/tree/master)
- Why 'official' Python is
  [wrong](https://github.com/AXGKl/unicode-kills-python3)
- UTF-8 [manifesto](http://utf8everywhere.org/#faq.python) about Python3

