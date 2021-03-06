# How to Handle Text In Python [M2M/IoT](http://en.wikipedia.org/wiki/Machine_to_machine) & Industrial Server Applications

## Axiros GmbH
May, 2015, Gunther Klessinger

<br>
<br>

- ``Esc``: Overview
- ``s``: Present
- ``STRG-` + STRG-[1-9] to sketch, STRG-[-=] width``

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


# "Whats the Problem, Why Should I Care?"

## Foreground Ok - Logfile Crashes

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

## no prob(?)

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

and 1000 of the like, typically pointing to Python3's unicode everywhere
model.

Which is the
[major](http://pyvideo.org/video/289/pycon-2010--mastering-python-3-i-o) compatibility breaker between 2 and 3.



# Offical 'Solution'

## Unicode Sandwich

Decode → Process → Encode. Everything.

<a href="http://nedbatchelder.com/text/unipain.html">
<img src="../images/sandwich.png" alt="sw" style="width: 450px;" />
</a>



## Feasible?

Think a second about what this means:

- **Humans** process text, expressed in *symbols* - which the unicode standard enumerates
  ongoingly into currently around 1Mio integers ("codepoints")
- **Systems** process, forward, store only bytes
- **[Standards](http://www.ietf.org/download/rfc-index.txt)** define how systems
  interact - unicode is next to irrelevant here, an [example](http://carl.sandiego.edu/bus188/osi_model.htm)
for layer6 in the OSI model.


## Standards Vs. Unicode

Any text identifier in any global standard is: **ASCII**.

By *definition* of being *global*.

Do risky conversions of ANY (possibly) text object?

    for k, v in my_payload.items():
        if isinstance(v, str):
            my_payload[k] = v.decode('utf-8') # is it utf-8?! Nesting?

For 'advantages' like this?

    >>> RAM, unic = sys.getsizeof, u' ' * 100000
    >>> round(float(RAM(unic)) / RAM(str(unic)), 2)
    4.0


## Decode = Irrelevant

The theory and idea behind having standards accepted, ratified, and agreed upon
by nations around the world, is to ensure that the system from country A will
be easily integrated with the system from country B with little effort.


"*While Unicode maps the BIGGEST POSSIBLE set of meaningful information for 
HUMANS, Standards define the SMALLEST NECESSARY, for SYSTEMS.*"

=> Non ASCII text values are typically just passed through, e.g. to storage.
Sometimes compared. Decoding required: Next to never!


## Human Text *Can* Be Hard

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


## But .decode() Alone Not The Solution

    #!/usr/bin/env python
    u1 = open('j1').read().decode('utf-8')
    u2 = open('j2').read().decode('utf-8')
    print u1, u2, isinstance(u1, unicode)
    print u1 == u2

    $ ./2.py
    José José True
    False

same, same...

*How text is entered & [interpreted](https://mathiasbynens.be/notes/javascript-unicode) by humans is [hard](http://utf8everywhere.org/#myth.strlen) - but irrelevant for inter
systems applications*



# The Better Way

## All Text Is Bytes

1. **All text is str() type**, i.e. usually exactly the bytes as they come in and
   have to go out, w/o any conversions at ingress or egress.
1. Encoding of **any** str() text object is **UTF-8** (which is equivalent to
   ASCII for identifiers)
1. Immediate encoding of **json** ``loads`` results to UTF-8.
1. We let Python convert types *implicitly*
1. Unicode only as intermittent functions - **if** required.

Note: This is also the way of Go, Rust and other modern languages built for inter systems communication.

## When to decode

- Counting number of symbols (but mind
  [normalization](https://dev.twitter.com/overview/api/counting-characters))
- upper(), lower(), capitalize()
- looping over symbols

Unicode knows about the 'meaning' of characters for humans:

    >>> s = 'José'; print '%s %s' % (s.upper(),unicode(s).upper())
    JOSé JOSÉ
    >>> for c in s: print c,
    J o s ? ?
    >>> for c in unicode(s): print c
    J o s é


## Defaultencoding

    >>> print '%s %s' % (s.upper(),unicode(s).upper())

No encode, decode - why did this not break, two times?

Python's does **implicit** type conversions for us - if we [configure it
right](http://www.ianbicking.org/illusive-setdefaultencoding.html):

## Configuration

At process setup time:

    if __name__ == '__main__':
        import sys; reload(sys); sys.setdefaultencoding('utf-8')

Better [Python wide](http://www.ianbicking.org/illusive-setdefaultencoding.html),
in ``site.py`` or ``sitecustomize.py``


. . .

And in packages' __init__, to enforce this:

    if 'ascii' in sys.getdefaultencoding().lower():
        raise Exception(("sys.defaultencoding on ASCII only! "
            "Axiros modules rely on full range implicit encoding."))




## Json

Json restricted itself to transferring human symbols only - via unicode
codepoints, on top of UTF-8 on the wire.

Why?
Javascript came from the human text processing world.


- Json is not an application protocol but a data exchange format, a 'carrier'
  of application data.
- A ``de-facto`` standard,now an RFC - for it's
  [obvious](http://www.json.org/fatfree.html) advantages, independent of
encoding.
- Safely convertable to UTF-8.

## Nested Encode

[Convert](https://github.com/axiros/nested_encode) any json right after loads
 (converter by [SH](https://github.com/stephan-hof), in C, perf. loss < 20%)

    >>> from nested_encode import encode_nested
    >>> encode_nested(json.loads(data))

- *Should* any other library (suds?) deliver unicode structures - convert same way.
- Py2 libraries normally deliver anyway byte strings as default.

# Problem Solved

## Python2 = Perfection

    s = 'é'; open('f', 'w').write(s)
    os.stat('f').st_size == len(s) # True
    '%s' % unicode(str(u'é')) == s # Works(!) & True
    print unicode('José').upper()  # Works, independent of stdout

- Ability to work with text 'as is', str(), unicode() **w/o type checking**
- **Implicit** conversions by Py2, allowing to write lean, simple, uncluttered, **[explicit](https://www.python.org/dev/peps/pep-0020/)**
  problem domain specific code
- .decode, .encode only for *special* situations: Mind the MS codepages
[fubar](https://github.com/AXGKl/unicode-kills-python3#bytes-without-a-meaning-the-ibmmicrosoft-codepage-fubar---and-its-relevance-today)
when receiving text from ancient times



## Links


- [This](https://github.com/axiros/unicode_in_axiros/blob/master/show.markdown)
  slide set
- UTF-8 [manifesto](http://utf8everywhere.org/#faq.python) about Python3
- [Tons of further information](https://github.com/AXGKl/unicode-kills-python3) incl. defaultencoding risk analysis and why
  I think Python3's unicode only design  nowadays is
  plain wrong (out-dated / risky / obsolete / [dies in
flames](http://lucumr.pocoo.org/2014/5/12/everything-about-unicode/))

##

<a href="http://lucumr.pocoo.org/2014/5/12/everything-about-unicode/">
<img src="../images/iopy3.png" alt="sw" style="border:0px; width: 90%;" />
</a>


## 

<a href="http://axiros.com">
<img src="../images/ax.png" alt="sw" style="border:0px; width: 200px;" />
</a>

