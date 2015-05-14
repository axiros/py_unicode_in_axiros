# Unicode In Axiros 
[Presentation 2015](https://axchange.axiros.com/multimedia/unicode/unicode_in_axiros/reveal.js/index.html#/text-in-axiros-python-processes) - why Py2.7 / bytestring sandwich / defaultencoding(utf-8)



## How to Create Other Presentations

### Technologies

- Format is [reveal.js](http://lab.hakim.se/reveal-js/#/)
- Source is [markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)
- Converter is pandoc => ``brew install pandoc``  (comes with reveal output template)

### Toolchain

    git clone https://github.com/axiros/unicode_in_axiros/
    ./make.py # in one terminal
    vi show.markdown # in another, write YOUR content
    file:///<path to unicode_in_axiros>/reveal.js/index.html # in browser to see presentation

- source is in show.markdown, free to modify.  [markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) works 
- ./make.py checks for changes of show.markdown and rebuilds reveal.js/index.html - which you open in the browser to see the presentation. make.py requires pandoc with reveal output plugin

It did not work out of box with the reveal.js version in this repo, so make.py inserts content into fitting index.html.tmpl

Structure of presentation must exactly follow this scheme:

- h1 (#) Only Title, no other text on slide
   - h2 (##) Title with content
   - h2 (##) Title with content
- h1 (#) Next Title
- (...)

No h3 allowed.

### Notes

- Check [impress.js](http://bartaz.github.io/impress.js/#/bored)
- CSS currently out of the box, would require some effort to allow more content on slides, scrolling and better CI
- Real cool would be [this](https://github.com/damianavila/RISE), i.e. the possibility to show live, working code, incl. updated charts, within the slideshow. 

But no time currently to have a look :-(



