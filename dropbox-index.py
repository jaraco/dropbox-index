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
__version__ = "0.3"

import sys
import os
import time
import locale

locale.setlocale(locale.LC_ALL, '')
LANG, ENCODING = locale.getlocale()

DATE_FORMAT = '%Y-%m-%d&nbsp;%H:%M:%S'

TABLE_HEADERS = {'en_GB': ('Name', 'Size', 'Last Modified'),
                 'pl_PL': ('Nazwa', 'Rozmiar', 'Czas modyfikacji')}

SCRIPT_WWW = 'http://code.google.com/p/kosciak-misc/wiki/DropboxInbox'

FILES_URL = 'http://dl.dropbox.com/u/69843/dropbox-index'

ICONS = (
    '%s/icons/back.png' % FILES_URL,
    '%s/icons/folder.png' % FILES_URL,
    '%s/icons/file.png' % FILES_URL,
    '%s/icons/image.png' % FILES_URL,
    '%s/icons/video.png' % FILES_URL,
    '%s/icons/music.png' % FILES_URL,
    '%s/icons/archive.png' % FILES_URL,
    '%s/icons/package.png' % FILES_URL,
    '%s/icons/pdf.png' % FILES_URL,
    '%s/icons/txt.png' % FILES_URL,
    '%s/icons/markup.png' % FILES_URL,
    '%s/icons/code.png' % FILES_URL,
    '%s/icons/font.png' % FILES_URL,
    '%s/icons/document.png' % FILES_URL,
    '%s/icons/spreadsheet.png' % FILES_URL,
    '%s/icons/presentation.png' % FILES_URL,
    '%s/icons/application.png' % FILES_URL,
    '%s/icons/plugin.png' % FILES_URL,
    '%s/icons/iso.png' % FILES_URL,
    )

FILE_TYPES = {
    ('gif', 'jpg', 'jpeg', 'png', 'bmp', 'tif', 'tiff', 'raw', 'img', 'ico', ): 'image',
    ('avi', 'ram', 'mpg', 'mpeg', 'mov', 'asf', 'wmv', 'asx', 'ogm', 'vob', '3gp', ): 'video',
    ('mp3', 'ogg', 'mpc', 'wav', 'wave', 'flac', 'shn', 'ape', 'mid', 'midi', 'wma', 'rm', 'aac', 'mka', ): 'music',
    ('tar', 'bz2', 'gz', 'arj', 'rar', 'zip', '7z', ): 'archive',
    ('deb', 'rpm', 'pkg', 'jar', 'war', 'ear', ): 'package', 
    ('pdf', ): 'pdf',
    ('txt', ): 'txt',
    ('html', 'htm', 'xml', 'css', 'rss', 'yaml', 'php', 'php3', 'php4', 'php5', ): 'markup',
    ('js', 'py', 'pl', 'java', 'c', 'h', 'cpp', 'hpp', 'sql', ): 'code',
    ('ttf', 'otf', 'fnt', ): 'font',
    ('doc', 'rtf', 'odt', 'abw', 'docx', 'sxw', ): 'document',
    ('xls', 'ods', 'csv', 'sdc', 'xlsx', ): 'spreadsheet',
    ('ppt', 'odp', 'pptx', ): 'presentation', 
    ('exe', 'msi', 'bin', 'dmg', ): 'application',
    ('xpi', ): 'plugin',
    ('iso', 'nrg', ): 'iso',
    }

STYLE = '''        
        body { font-family: Verdana, sans-serif; font-size: 12px;}
        a { text-decoration: none; color: #00A; }
        a:hover { text-decoration: underline; }
        h1 { padding: 0; margin: 0.5em auto 0.5em 1em; }
        table { text-align: center; margin: 0 auto 0 1.5em; border-collapse: collapse; }
        thead { border-bottom: 1px solid #555; }
        th:hover { cursor: pointer; cursor: hand; background-color: #EEE; }
        #direction { border: 0; vertical-align: bottom; margin: 0 0.5em;}
        tbody { border-bottom: 1px solid #555;}
        tr, th { line-height: 1.7em; min-height: 25px; }
        tbody tr:hover { background-color: #EEE; }
        .name { text-align: left; width: 35em; }
        .name a, thead .name { padding-left: 22px; }
        .name a { display: block; }
        .size { text-align: right; width: 7em; padding-right: 1em;}
        .date { text-align: right; width: 15em; padding-right: 1em;}
        #footer { margin: 1em auto 0.5em 2em; font-size: smaller;}
        /* Icons */
        .dir, .back, .file { background-repeat: no-repeat; background-position: 2px 4px;}
        .back { background-image: url('%s'); }
        .dir { background-image: url('%s'); }
        .file { background-image: url('%s'); }
        .image { background-image: url('%s'); }
        .video { background-image: url('%s'); }
        .music { background-image: url('%s'); }
        .archive { background-image: url('%s'); }
        .package { background-image: url('%s'); }
        .pdf { background-image: url('%s'); }
        .txt { background-image: url('%s'); }
        .markup { background-image: url('%s'); }
        .code { background-image: url('%s'); }
        .font { background-image: url('%s'); }
        .document { background-image: url('%s'); }
        .spreadsheet { background-image: url('%s'); }
        .presentation { background-image: url('%s'); }
        .application { background-image: url('%s'); }
        .plugin { background-image: url('%s'); }
        .iso { background-image: url('%s'); }''' % ICONS

JAVASCRIPT = '''
    function sort() {
        column = $(this).attr("class").split(' ')[0];
        $("#direction").remove();
        if ($(this).hasClass("desc")) {
            $("#dropbox-index-list thead tr th").each(function(i) { $(this).removeClass("asc").removeClass("desc") });
            $(this).addClass("asc");
            reverse = -1;
        } else {
            $("#dropbox-index-list thead tr th").each(function(i) { $(this).removeClass("asc").removeClass("desc") });
            $(this).addClass("desc");
            reverse = 1;
        }
        if (column == "name") {
            $(this).append('<img src="%s/icons/'+((reverse == 1) ? 'desc' : 'asc')+'.png" id="direction" />');
        } else {
            $(this).prepend('<img src="%s/icons/'+((reverse == 1) ? 'desc' : 'asc')+'.png" id="direction" />');
        }
        rows = $("#dropbox-index-list tbody tr").detach()
        rows.sort(function(a, b) {
            result = $(a).data('type') - $(b).data('type')
            if (result != 0) { return result }
            
            return (($(a).data(column) < $(b).data(column)) - ($(a).data(column) > $(b).data(column))) * reverse
            
        });
        $("#dropbox-index-list tbody").append(rows);
    }
    
    function prepare() {
        $("#dropbox-index-list tbody tr").each(function(i) {
            if ($(this).children(".name").hasClass("back")) {
                $(this).data('type', 1);
            } else if ($(this).children(".name").hasClass("dir")) {
                $(this).data('type', 2);
            } else {
                $(this).data('type', 3);
            }
            $(this).data('name', $(this).children(".name").text().toLowerCase());
            $(this).data('size', parseInt($(this).children(".size").attr("sort")));
            $(this).data('date', parseInt($(this).children(".date").attr("sort")));
        });
        
        $("#dropbox-index-list thead tr th").each(function(i) {
            $(this).bind('click', sort);
        });
    }

    $(document).ready(function(){
        prepare();
    });
''' % (FILES_URL, FILES_URL)

HTML_START = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=%s"/> 
    <title>%s</title>
    <link rel="shortcut icon" href="%s/icons/favicon.ico"/>
    <style>%s</style>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
    <script>%s</script>
</head>
<body>
'''
HTML_HEADER = '<h1>%s</h1>'
HTML_TABLE = '''
<table id="dropbox-index-list">
    <thead>
        <tr>
            <th class="name">%s</th><th class="size">%s</th><th class="date">%s</th>
        </tr>
    </thead>
    <tbody>
'''
HTML_BACK = '<tr><td class="name back"><a href="../index.html">..</a></td><td class="size">&nbsp;</td><td class="date">&nbsp;</td></tr>'
HTML_DIR = '<tr><td class="name dir"><a href="%(file_name)s/index.html">%(file_name)s</a></td><td class="size">&nbsp;</td><td class="date" sort="%(file_time_sort)s">%(file_time)s</td></tr>\n'
HTML_FILE = '<tr><td class="name file%(file_type)s"><a href="%(file_name)s">%(file_name)s</a></td><td class="size" sort="%(file_size_sort)s">%(file_size)s</td><td class="date" sort="%(file_time_sort)s">%(file_time)s</td></tr>\n'
HTML_END = '''
    </tbody>
</table>
<div id="footer">
Generated on <strong>%s</strong> using <a href="%s">Dropbox-index</a>-%s</a>
</div>
</body>
</html>'''


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


def get_filetype(file_name):
    filetype = file_name.split('.')[-1].lower()
    for keys, value in FILE_TYPES.items():
        if filetype in keys:
            return ' %s' % value
    return ''


def html_render(path, back, dirs, files):
    PATH = os.path.basename(os.path.realpath(path))
    
    index = open(os.path.join(path, 'index.html'), 'w')
    index.write(HTML_START % (ENCODING, PATH, FILES_URL, STYLE, JAVASCRIPT))
    index.write(HTML_HEADER % PATH)
    index.write(HTML_TABLE % table_headers())
    
    if back:
        index.write(HTML_BACK)
    
    for file in dirs:
        file_name = os.path.basename(file)
        file_time = time.strftime(DATE_FORMAT, time.localtime(os.path.getmtime(file)))
        file_time_sort = os.path.getmtime(file)
        index.write(HTML_DIR % locals())
        
    for file in files:
        file_name = os.path.basename(file)
        file_type = get_filetype(file_name)
        file_size = get_size(file)
        file_size_sort = os.path.getsize(file)
        file_time = time.strftime(DATE_FORMAT, time.localtime(os.path.getmtime(file)))
        file_time_sort = os.path.getmtime(file)
        index.write(HTML_FILE % locals())
    
    now = time.strftime(DATE_FORMAT, time.localtime())
    index.write(HTML_END % (now, SCRIPT_WWW, __version__))
    
   

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
