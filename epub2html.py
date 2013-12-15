#!/usr/bin/env python

#  The MIT License (MIT)
# 
#  Copyright (c) 2013 Adrian Vollmer
# 
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
# 
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
# 
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

version = "0.1"

# Convention: all *_dir and *_file variables must contain the full path to
# the directory or file they are referring to


import os
import sys
import subprocess
import argparse
from shutil import copyfile
from xml.dom.minidom import parseString, Document


search_dirs = [ os.path.dirname(os.path.realpath(__file__)) + "/",
    os.path.expanduser("~") + '/.epub2html/',
    '/usr/share/epub2html/' ]


def get_xml(filename):
    """Read an XML file and return the DOM tree."""
    f = file(filename) 
    data = f.read()
    f.close()
    return parseString(data)
 

def parse_cli_options():
    """Process the command line arguments."""
    parser = argparse.ArgumentParser(description="Convert an ebook from" +
        "epub format to html", version="%prog version " + version)
    parser.add_argument("-b", "--browser", dest="browser",
          help="starts a browser to display the ebook")
    parser.add_argument("-c", "--css", dest="css",
          help="include a custom CSS file")
    parser.add_argument("-j", "--jquery", dest="jquery",
          help="include a custom jquery.js file")
    parser.add_argument("-d", "--dropdown", dest="dropdown",
          help="include a custom dropdown.js file")
    parser.add_argument("epub", help="name of the .epub file")
    return parser.parse_args()


def get_input_file(book_file, filename, path=None):
    """Copies a file from one of the default paths to the ebook path and returns the new path."""
    if (path == None):
        try: 
            input_file = [f + filename for f in search_dirs
                        if os.path.exists(f + filename )][0]
        except IndexError:
            print "File '" + filename + "' not found in either of these directories:"
            for d in search_dirs:
                print d
            exit()
    else:
        input_file = path + filename

    dest = os.path.dirname(book_file) + "/" + filename

    copyfile(input_file, dest)

    return filename


def get_opf(epub_dir):
    """Read the container XML file at epub_dir and return the path of the *.opf file."""
    dom = get_xml(epub_dir + 'META-INF/container.xml')
    xmlTag = dom.getElementsByTagName('rootfile')[0]
    return xmlTag.attributes['full-path'].value


# Get meta info: Author, Title, ...
# TODO


def get_toc(root_file):
    """Return the filename of the file containing the table of contents."""
    dom = get_xml(root_file)
    xmlTag = dom.getElementsByTagName('manifest')[0].getElementsByTagName('item')
    for node in xmlTag:
        if (node.attributes['id'].value == "ncx"):
          toc_file = node.attributes['href'].value
          break
    root_dir = os.path.dirname(root_file) + "/"
    return root_dir + toc_file


def extract_content(root_dir, opf_file):
    dom = get_xml(opf_file)
    xmlTag = dom.getElementsByTagName('package')[0].\
                getElementsByTagName('spine')[0].getElementsByTagName('itemref')
    spinelist = [node.attributes['idref'].value for node in xmlTag]

    xmlTag = dom.getElementsByTagName('package')[0].\
                getElementsByTagName('manifest')[0].getElementsByTagName('item')
    manifest = {}
    for node in xmlTag:
        manifest[node.attributes['id'].value] = node.attributes['href'].value

    content = []
    for ref in spinelist:
        chap = [root_dir + manifest[ref]]
        xmlTag = get_xml(chap[0])
        for node in xmlTag.getElementsByTagName('body')[0].childNodes:
            chap.append(node)
        content.append(chap)
    return content
        

def get_chapter_list(epub_dir, root_dir, toc_file):
    """Build a list containing chapter names, their filenames, etc."""
    table_of_contents = []
    dom = get_xml(toc_file)
    xmlTag = dom.getElementsByTagName('navMap')[0].getElementsByTagName('navPoint')
    for node in xmlTag:
        chapter_title = node.getElementsByTagName('navLabel')[0].\
                    getElementsByTagName('text')[0].childNodes[0].nodeValue
        chapter_link = node.getElementsByTagName('content')[0].\
                    attributes['src'].value
        if ('#' in chapter_link):
            (chapter_file, chapter_anchor) = (root_dir + chapter_link).split('#')
        else:
            chapter_file   = root_dir + chapter_link
            chapter_anchor = ''
        table_of_contents.append([chapter_title,
                                  chapter_file, chapter_anchor])

    return table_of_contents
 

# Compile chapters

# The structure is going to be:
#
# <html>
# <head>
# [insert header from the ebook (from the first file)]
# [insert own css]
# [insert own js]
# </head>
# <body>
# <div class="header">
#    [TABLE OF CONTENTS dropdown menu]
# </div>
# <div class=content>
#    [insert invidiual chapters from the ebook]
# </div></body></html>



def make_head(doc, args, table_of_contents, epub_dir, book_file):
    """Build the XML "head" tag."""
    head_tag = doc.createElement('head')
        # get the head of the second file (the first file is sometimes just
        # a picture of the cover and doesn't have a CSS)
    xmlTag = get_xml(table_of_contents[1][1])
    head_tag = xmlTag.getElementsByTagName('head')[0]

        # now attach css tag
    css_tag = doc.createElement('link')
    css_tag.attributes['type'] = 'text/css'
    css_file = get_input_file(book_file, "default.css", args.css)
    css_tag.attributes['href'] = css_file
    css_tag.attributes['rel'] = "stylesheet"
    head_tag.appendChild(css_tag)

        # now attach jquery script tag
    script1_tag = doc.createElement('script')
    script1_tag.attributes['type'] = 'text/javascript'
    jquery_file = get_input_file(book_file, "jquery.js", args.jquery)
    script1_tag.attributes['src'] = jquery_file
    script1_tag.appendChild(doc.createTextNode(' '))
    head_tag.appendChild(script1_tag)

        # now attach dropdown script tag
    script2_tag = doc.createElement('script')
    script2_tag.attributes['type'] = 'text/javascript'
    dropdown_file = get_input_file(book_file, "dropdown.js", args.dropdown)
    script2_tag.attributes['src'] = dropdown_file 
    script2_tag.appendChild(doc.createTextNode(' '))
    head_tag.appendChild(script2_tag)

    return head_tag


def make_body(doc, table_of_contents, contents):
    """Build the XML "body" tag."""
    body_tag = doc.createElement('body')

        # build a TOC menu
    header_tag = doc.createElement('div')
    header_content_tag = doc.createElement('div')
    header_tag.attributes['class'] = 'header'
    header_content_tag.attributes['class'] = 'header-cont'

    ul1_tag = doc.createElement('ul')
    ul1_tag.attributes['class'] = 'dropdown'
    li1_tag = doc.createElement('li')
    a1_tag = doc.createElement('a')
    a1_tag.attributes['href'] = '#'
    a1_tag.appendChild(doc.createTextNode('Contents'))
    li1_tag.appendChild(a1_tag)
    ul2_tag = doc.createElement('ul')
    ul2_tag.attributes['class'] = 'sub_menu'

        # add the links to each individual chapter to the TOC menu
    for chap in table_of_contents:
        li2_tag = doc.createElement('li')
        a2_tag = doc.createElement('a')
        if (len(chap[2]) > 0):
            a2_tag.attributes['href'] = '#' +  chap[2]
        else:
            a2_tag.attributes['href'] = '#' + chap[1]  + chap[2]
        a2_tag.appendChild(doc.createTextNode(chap[0]))
        li2_tag.appendChild(a2_tag)
        ul2_tag.appendChild(li2_tag)

    li1_tag.appendChild(ul2_tag)

    ul1_tag.appendChild(li1_tag)
    header_content_tag.appendChild(ul1_tag)
    header_tag.appendChild(header_content_tag)
    body_tag.appendChild(header_tag)

        # now insert the chapters
    content_tag = doc.createElement('div')
    content_tag.attributes['class'] = 'content'

        # Fill in the content 
    inserted_chapters = []
    for chap in contents:
        # insert anchor here
        anchor_tag = doc.createElement('a')
        anchor_tag.attributes['id'] = chap[0]
        content_tag.appendChild(anchor_tag)
        # now append all the <p>'s and so on
        for node in chap[1:]:
            content_tag.appendChild(node)
    body_tag.appendChild(content_tag)
    return body_tag

# TODO fix links. All links in the original document point to anchors in
# other files.


def main():
    args = parse_cli_options()

    epub_file = args.epub
    epub_dir = "epub-" + str(abs(hash(epub_file))) + "/"

        # Extract files from the epub
    subprocess.call(["unzip", "-qo", epub_file, "-d", epub_dir])

        # Extract information from the epub files
    root_file = epub_dir + get_opf(epub_dir)
    root_dir = os.path.dirname(root_file) + "/"

    toc_file = get_toc(root_file)
    contents = extract_content(root_dir, root_file)
    
    table_of_contents = get_chapter_list(epub_dir, root_dir, toc_file)

    book_file = os.path.dirname(table_of_contents[0][1]) + "/book.html"
    # lets hope all chapter files are in the same directory

        # Now build the new document
    doc = Document()
    html_tag = doc.createElement('html')
    doc.appendChild(html_tag)

    html_tag.appendChild(make_head(doc, args, table_of_contents, epub_dir, book_file))
    html_tag.appendChild(make_body(doc, table_of_contents, contents))

        # write DOM to file
    with open(book_file, 'w') as f:
        f.write(doc.toprettyxml().encode('utf8'))

        # delete the old html files. they only take up space
    for chap in contents:
        try: 
            os.remove(chap[0])
        except OSError:
            pass

    # pass the html page to the browser if one was specified
    if (args.browser!=None):
        subprocess.call([args.browser, book_file])


if __name__ == "__main__":
    main()
