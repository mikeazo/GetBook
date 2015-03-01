# This script generates ePub files from the books made 
# available by the Neal A. Maxwell Institute for 
# Religious Scholarship at Brigham Young University 
# (http://maxwellinstitute.byu.edu/).
# Run the script by passing the bookid from the book's url as an argument
# e.g. for _Temple and the Cosmos_ 
# (http://maxwellinstitute.byu.edu/publications/books/?bookid=103), 
# use the command'python GetBook.py 103'

# Script created by Matt Turner (http://guavaduck.com/)

import urllib
import re
import os
import zipfile
import glob
import shutil
import sys
import tidy
import codecs 
import platform
from pyquery import PyQuery

#import pdb # For debugging

class URLopener(urllib.FancyURLopener):
    version = 'GetBook.py/0.1 '+platform.platform()+' (+http://guavaduck.com/)'
urlopener=URLopener()

print '--'
print 'Maxwell Institute Book to ePub Converter'
print 'by Matt Turner (http://guavaduck.com/)'
print '--'
print ''

create_book=False
create_epub=False

for arg in sys.argv:
    try:
        int(arg)
        book_id=arg
    except:
        pass
    if arg=='book':
        create_book=True
    if arg=='epub':
        create_epub=True
        
if not book_id:
    book_id=raw_input('Book id? ')
if create_book==False:
    create_epub=True

book_url='http://publications.maxwellinstitute.byu.edu/fullscreen/?pub='+book_id

f=urlopener.open(book_url)
#f=open('sample_book.html')
s=f.read()

d = PyQuery(s)

book_title = d('#print-title').text().replace('>', '').strip()
print book_title
book_author = d('#print-author').text().replace('by:', '').strip()
if not book_author:
    book_author="Unknown"
print book_author

print 'Retrieving _'+book_title+'_ by '+book_author

# find the  chapters
chapters = d('#fullscreen-toc-content a')
n_chapters=len(chapters)
chapter_titles=[c.text for c in chapters]
chapter_texts=['']*n_chapters

xhtml_options = dict(output_xhtml=1, add_xml_decl=1, indent=1, tidy_mark=0, char_encoding='utf8', clean=1, numeric_entities=1,enclose_block_text=1,doctype='strict',anchor_as_name=0)
xml_options = dict(indent=1, tidy_mark=0, numeric_entities=1,input_xml=1)

for n in range(1, n_chapters+1):
    print 'Retrieving chapter '+str(n)+' of '+str(n_chapters)
    chapter_url=book_url+'&index='+str(n)
    f=urlopener.open(chapter_url)
    s_chapter=f.read()
    d_chapter = PyQuery(s_chapter)
    chapter_text = d_chapter('#html-content').html() 
    chapter_texts[n-1]=re.sub('\n','\n\t\t',chapter_text)
    f.close()
    try:
        print '    '+chapter_titles[n-1]
    except:
        print '    '+chapter_titles[n-1].encode('ascii', 'replace')
    
book_path=re.sub('[^a-zA-Z0-9\-_.() ]',' ',book_title)+'.'+book_id
book_path0=book_path+''
n_path=0

while os.path.exists(book_path) or os.path.exists(book_path+'.epub'):
    n_path+=1
    book_path=book_path0+'.'+str(n_path)

os.mkdir(book_path)
os.chdir(book_path)

os.mkdir('source')
os.chdir('source')

f=codecs.open('title.xhtml','w','utf-8')
f.write(str(tidy.parseString('<html>\n\t<head>\n\t\t<title>'+book_title+'</title>\n\t\t<link rel="stylesheet" type="text/css" href="style.css" />\n\t</head>\n\t<body>\n\t\t<div id="book_title"><h1>'+book_title+'</h1>\n\t\t<h2>by '+book_author+'</h2></div>\n\t</body>\n</html>', **xhtml_options)))
f.close()

for n in range(n_chapters):
    f=open('chapter'+str(n)+'.xhtml','w')
    f.write(str(tidy.parseString(('<html>\n\t<head>\n\t\t<title>'+chapter_titles[n]+'</title>\n\t\t<link rel="stylesheet" type="text/css" href="style.css" />\n\t</head>\n\t<body>\n\t\t<div id="chapter_title"><h1>'+chapter_titles[n]+'''</h1></div>\n\t\t'''+chapter_texts[n]+'\n\t</body>\n</html>').encode('utf-8'), **xhtml_options)))
    f.close()
    
os.chdir('..')

if create_epub:
    f=open('mimetype','w')
    f.write('application/epub+zip')
    f.close()

    os.mkdir('META-INF')
    os.chdir('META-INF')
    f=open('container.xml','w')
    f.write('''<?xml version="1.0"?>
    <container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
      <rootfiles>
        <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
      </rootfiles>
    </container>''')
    f.close()
    os.chdir('..')

    os.mkdir('OEBPS')
    os.chdir('OEBPS')
    f=codecs.open('content.opf','w','utf-8')
    f.write('''<?xml version="1.0"?>
    <package version="2.0" xmlns="http://www.idpf.org/2007/opf"
             unique-identifier="BookId">
     <metadata xmlns:dc="http://purl.org/dc/elements/1.1/"
               xmlns:opf="http://www.idpf.org/2007/opf">
       <dc:title>'''+book_title+'''</dc:title> 
       <dc:creator opf:role="aut">'''+book_author+'''</dc:creator>
       <dc:language>en-US</dc:language> 
       <dc:identifier id="BookId">urn:uuid:'''+book_url+'''</dc:identifier>
     </metadata>
     <manifest>
      <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml" />
      <item id="stylesheet" href="style.css" media-type="text/css"/>
      <item id="title" href="title.xhtml" media-type="application/xhtml+xml"/>''')

    for n in range(n_chapters):
        f.write('''
      <item id="chapter'''+str(n)+'''" href="chapter'''+str(n)+'''.xhtml" media-type="application/xhtml+xml"/>''')
      
    f.write('''
     </manifest>
     <spine toc="ncx">
      <itemref idref="title"/>''')
     
    for n in range(n_chapters):
        f.write('''
      <itemref idref="chapter'''+str(n)+'''"/>''')

    f.write('''
     </spine>
    </package>''')
    f.close()

    toc_string = '''<?xml version="1.0" encoding="UTF-8"?>
    <ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
      <head>
        <meta name="dtb:uid" content="'''+book_url+'''"/>
        <meta name="dtb:depth" content="1"/>
        <meta name="dtb:totalPageCount" content="0"/>
        <meta name="dtb:maxPageNumber" content="0"/>
      </head>
      <docTitle>
        <text>'''+book_title+'''</text>
      </docTitle>
      <navMap>
        <navPoint id="title" playOrder="1">
          <navLabel>
            <text>Title Page</text>
          </navLabel>
          <content src="title.xhtml"/>
        </navPoint>'''
        
    for n in range(n_chapters):
        toc_string=toc_string+'''
        <navPoint id="chapter'''+str(n)+'''" playOrder="'''+str(n+2)+'''">
          <navLabel>
            <text>'''+chapter_titles[n]+'''</text>
          </navLabel>
          <content src="chapter'''+str(n)+'''.xhtml"/>
        </navPoint>'''

    toc_string=toc_string+'''
      </navMap>
    </ncx>'''

    f=codecs.open('toc.ncx', 'w', 'utf-8')
    f.write(str(tidy.parseString((toc_string).encode('utf-8'),**xml_options)))
    f.close()
    
    for name in glob.glob("../source/*"):
        shutil.copy(name,'./')
        
    f=open('style.css','w')
    f.close()

    os.chdir('../..')

    file = zipfile.ZipFile(book_path+'.epub', "w")
    os.chdir(book_path)
    file.write('mimetype','mimetype',zipfile.ZIP_STORED)
    file.write('META-INF/container.xml','META-INF/container.xml',zipfile.ZIP_DEFLATED)
    #file.write('META-INF/container.xml','META-INF/container.xml',zipfile.ZIP_STORED)
    for name in glob.glob("OEBPS/*"):
        file.write(name,name,zipfile.ZIP_DEFLATED)
    #    file.write(name,name,zipfile.ZIP_STORED)
    file.close()
    
    shutil.rmtree('META-INF')
    shutil.rmtree('OEBPS')
    os.remove('mimetype')
    os.chdir('..')
    
if create_book:

    os.chdir('source')
    f = open('copyright.xhtml','w')
    f.close()
    os.chdir('..')
    
    f = codecs.open(book_path+'.book','w','utf-8')
    f.write('Title: '+book_title+'\n')
    f.write('Author: '+book_author+'\n')
    f.write('URL: '+book_url+'\n')
    f.write('Language: en\nCover: source/cover.jpg\nCSS: source/style.css\n\n')
    f.write('Title Page | source/title.xhtml\n')
    f.write('Copyright | source/copyright.xhtml\n')
    
    for n in range(n_chapters):
        f.write('Chapter '+str(n)+' - '+chapter_titles[n]+' | source/chapter'+str(n)+'.xhtml\n')
    
    f.close
    
if not create_book:
    shutil.rmtree(book_path)
