# Unicode In Axiros 
[Presentation 2015](https://axchange.axiros.com/multimedia/unicode/unicode_in_axiros/reveal.js/index.html#/text-in-axiros-python-processes) - why Py2.7 / bytestring sandwich / defaultencoding(utf-8)

Watch the presentation [here](https://axchange.axiros.com/multimedia/unicode/unicode_in_axiros/reveal.js/index.html#/text-in-axiros-python-processes)


## How to Create Other Presentations

- source is in show.markdown, free to modify. Check how [markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) works 
- ./make.py checks for changes of show.markdown and rebuilds reveal.js/index.html - which you open in the browser to see the presentation
- ./make.py requires pandoc with reveal output plugin

=> brew install pandoc 

It did not work out of box with the reveal.js version in this repo, so make.py inserts content into fitting index.html.tmpl

Structure of presentation must exactly follow this scheme:

h1 (#) Only Title, no other text on slide
   h2 (##) Title with content
   h2 (##) Title with content
h1 (#) Next Title

No h3 allowed.





