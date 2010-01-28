#!/usr/bin/env python
#
# Copyright 2010 Wojciech 'KosciaK' Pietrzok
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ----------------------------------------------------------------------
#
# Icons used:
# famfamfam's "Silk" icon set - http://www.famfamfam.com/lab/icons/silk/
#

__author__ = "Wojciech 'KosciaK' Pietrzok (kosciak@kosciak.net)"
__version__ = "0.1"

import sys
import os
import time
import locale

locale.setlocale(locale.LC_ALL, '')
LANG, ENCODING = locale.getlocale()
DATE_FORMAT = '%Y-%m-%d&nbsp;&nbsp;&nbsp;%H:%M:%S'
TABLE_HEADERS = {'en_GB': ('Name', 'Size', 'Last Modified'),
                 'pl_PL': ('Nazwa', 'Rozmiar', 'Czas modyfikacji')}
SCRIPT_WWW = 'http://code.google.com/p/kosciak-misc/wiki/DropboxInbox'
ICON_URL = 'http://dl.dropbox.com/u/69843/dropbox-index'
FILE_ICON_URL = '%s/file.png' % ICON_URL
FOLDER_ICON_URL = '%s/folder.png' % ICON_URL


def table_headers():
    if LANG in TABLE_HEADERS:
        return TABLE_HEADERS[LANG]
    else:
        return TABLE_HEADERS['en_GB']
    

def get_size(file):
    size = os.path.getsize(file)
    
    if size < 1000:
        return '%s bytes' % size
    
    kilo = size / 1024
    if kilo < 1000:
        return '%s KB' % round(float(size) / 1024, 1)
    
    mega = kilo / 1024
    return '%s MB' % round(float(kilo) / 1024, 1)


def html_render(path, back, dirs, files):
    index = open(os.path.join(path, 'index.html'), 'w')
    index.write('''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=%s"/> 
    <title>%s</title>''' % (ENCODING, os.path.basename(os.path.realpath(path))))
    
    index.write('''<style>
        body { font-type: sans-serif; }
        a { text-decoration: none; }
        a:hover { text-decoration: underline; }
        table { text-align: center; margin: 0 auto 0 1.5em; border-collapse: collapse; }
        thead { border-bottom: 1px solid #555; }
        tr { line-height: 1.7em; min-height: 25px; }
        tbody tr:hover { background-color: #EEE; }
        .name { text-align: left; width: 35em; padding-left: 22px; }
        .name a {display: block; }
        .size { text-align: right; width: 7em;}
        .date { text-align: right; width: 15em; padding-right: 0.5em;}
        .dir, .back { background-image: url('%s'); background-repeat: no-repeat; background-position: 2px 4px;}
        .file { background-image: url('%s'); background-repeat: no-repeat; background-position: 2px 4px;}
        #footer { border-top: 1px solid #555; margin: 3em 1em 0 1em; padding: 0.5em; font-size: x-small; }
    </style>
</head>
<body>\n''' % (FOLDER_ICON_URL, FILE_ICON_URL))
    
    index.write('<h1>%s</h1>' % os.path.basename(os.path.realpath(path)))
    
    index.write('''
<table>
    <thead>
        <tr>
            <th class="name">%s</th><th class="size">%s</th><th class="date">%s</th>
        <tr>
    </thead>
    <tbody>\n''' % table_headers())
    
    if back:
        index.write('<tr class="back"><td class="name"><a href="../index.html">..</a></td><td class="size">&nbsp;</td><td class="date">&nbsp;</td></tr>')
    
    for file in dirs:
        file_name = os.path.basename(file)
        file_time = time.strftime(DATE_FORMAT, time.localtime(os.path.getmtime(file)))
        index.write('<tr class="dir"><td class="name"><a href="%s/index.html">%s</a></td><td class="size">&nbsp;</td><td class="date">%s</td></tr>\n' % (file_name, file_name, file_time))
        
    for file in files:
        file_name = os.path.basename(file)
        file_size = get_size(file)
        file_time = time.strftime(DATE_FORMAT, time.localtime(os.path.getmtime(file)))
        index.write('<tr class="file"><td class="name"><a href="%s">%s</a></td><td class="size">%s</td><td class="date">%s</td></tr>\n' % (file_name, file_name, file_size, file_time))
    
    index.write('''
    </tbody>
<table>
<div id="footer">
Generated using <a href="%s">Dropbox-index</a> %s by <a href="http://kosciak.blox.pl/">Wojciech 'KosciaK' Pietrzok</a>
</div>
</body>
</html>''' % (SCRIPT_WWW, __version__))
    
   

def crawl(path, back=None, recursive=False):
    if not os.path.exists(path):
        print 'Path %s does not exists' % path
        return
    
    if not os.path.isdir(path):
        print 'Path %s is not a directory' % path
        return
    
    # get contents of the directory
    contents = [os.path.join(path, file) for file in os.listdir(path) if not file.endswith('index.html')]
    # remove hidden files
    # TODO: identify Windows hidden files
    contents = [file for file in contents if not os.path.basename(file).startswith('.')]
    
    # get only files
    files = [file for file in contents if os.path.isfile(file)]
    files.sort(key=str.lower)
    
    # get only directories
    if recursive:
        dirs = [file for file in contents if os.path.isdir(file)]
        dirs.sort(key=str.lower)
    else:
        dirs = [];
    
    # render directory contents
    html_render(path, back, dirs, files)

    print 'Created index.html for %s' % os.path.realpath(path)

    # crawl subdirectories
    for dir in dirs:
        crawl(dir, path, recursive)
    


if __name__ == '__main__':
    
    HELP = '''Usage: dropbox-index.py [options] <directory>

Options:
  -h, --help            Show help message and exit.
  -R, --recursive       Include subdirectories (disabled by default).\n'''
    
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help']:
            print HELP
        elif sys.argv[1] in ['-R', '--recursive']:
            if len(sys.argv) > 2:
                crawl(sys.argv[2], recursive=True)
            else:
                print 'ERROR: No directory specified'
                print HELP
        else:
            crawl(sys.argv[1])
        
    else:
        print HELP
