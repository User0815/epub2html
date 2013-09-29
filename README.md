What is this?
=============

`epub2html` is a Python script that converts ebooks in the EPUB format to
a HTML file. 


Why would I need this?
======================

Sometimes I enjoy reading an ebook on my computer. While there are a few
ebook viewers for GNU/Linux, none of them felt satisfactory to me. Calibre
is much more than just a viewer and total overkill for my purposes. FBReader
is nice in principle, but it's rather limited in configurability -- when it
comes to custom hotkeys or custom layout, for example. Plus, it forces a new
page when you scroll to a new chapter, which felt rather awkward. One
command line ebook viewer had the same problem, it could only display one
individual chapter at a time.

That's when I decided to make my own ebook viewer. Since the epub format is
essentially a zip file of HTML files, it's a natural choice to use the
browser for viewing. You usually spend a lot of time in your browser, so you
know how to operate it, how to customize it, etc. Unfortunately there was no
plugin for reading ebooks available for my favorite browser, which is Opera.

Thus, this script was born. It compiles all chapters into a single HTML file
with a CSS file of your choice. You can even use Lynx or elinks to view the
ebook on the command line this way.


It doesn't work for my favorite ebook!
======================================

I'm no expert on the epub standard, and while I tested it with the EPUB
files I have available, yours may behave differently than the ones I tested.
Just let me know what the problem is, ideally with a copy of the offending
file, and I'll take a look.


License
=======

The MIT License (MIT)

Copyright (c) 2013 Adrian Vollmer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

