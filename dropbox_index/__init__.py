"""
Icons used:
famfamfam's "Silk" icon set - http://www.famfamfam.com/lab/icons/silk/

>>> target = getfixture('sample_dir')
>>> crawl(target, recursive=True)
Created index.html for ...
>>> crawl(target, template_file=getfixture('template_file'))
Created index.html for ...
"""

import os
import os.path
import re
import time
import locale
import pathlib
import argparse
from importlib import metadata

import importlib_resources as resources


locale.setlocale(locale.LC_ALL, '')
LANG, ENCODING = locale.getlocale()

DATE_FORMAT = '%Y-%m-%d&nbsp;%H:%M:%S'

TABLE_HEADERS = {
    'en_GB': ('Name', 'Size', 'Last Modified'),
    'pl_PL': ('Nazwa', 'Rozmiar', 'Czas modyfikacji'),
}

SCRIPT_WWW = 'https://pypi.org/project/dropbox-index'

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


def _load_file_types():
    with resources.files().joinpath('types.txt').open(encoding='utf-8') as stream:
        for line in stream:
            type, _, exts = line.partition(':')
            for ext in re.findall(r'\w+', exts):
                yield ext, type


FILE_TYPES = dict(_load_file_types())

HTML_STYLE = (
    resources.files().joinpath('style.html').read_text(encoding='utf-8') % ICONS
)


JAVASCRIPT = (
    resources.files()
    .joinpath('logic.js')
    .read_text(encoding='utf-8')
    .replace('FILES_URL', FILES_URL)
)
HTML_JAVASCRIPT = f"""
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
    <script>
    {JAVASCRIPT}
    </script>
    """

FAVICON = '<link rel="shortcut icon" href="%s/icons/favicon.ico"/>' % FILES_URL

HTML_START = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset="%(ENCODING)s"/>
    <title>%(PATH)s</title>
    %(FAVICON)s
    %(HTML_STYLE)s
    %(HTML_JAVASCRIPT)s
</head>
<body>
'''
HTML_HEADER = '<h1 id="dropbox-index-header">%s</h1>'
HTML_TABLE_START = '''
<table id="dropbox-index-list">
    <thead>
        <tr>
            <th class="name">%s</th><th class="size">%s</th><th class="date">%s</th>
        </tr>
    </thead>
    <tbody>
'''
HTML_BACK = (
    '<tr><td class="name back"><a href="../index.html">'
    '..</a></td><td class="size">&nbsp;</td><td class="date">&nbsp;</td></tr>'
)
HTML_DIR = (
    '<tr><td class="name dir"><a href="%(file_name)s/index.html">'
    '%(file_name)s</a></td><td class="size">&nbsp;</td>'
    '<td class="date" sort="%(file_time_sort)s">%(file_time)s</td></tr>\n'
)
HTML_FILE = (
    '<tr><td class="name file%(file_type)s"><a href="%(file_name)s">'
    '%(file_name)s</a></td><td class="size" sort="%(file_size_sort)s">'
    '%(file_size)s</td><td class="date" sort="%(file_time_sort)s">'
    '%(file_time)s</td></tr>\n'
)
HTML_TABLE_END = '''
    </tbody>
</table>
<div id="dropbox-index-footer">Generated on <strong>%s</strong> using
<a href="%s">Dropbox-index</a>-%s</a></div>'''
HTML_DIR_INFO = '''
<div id="dropbox-index-dir-info">
%(DIR_INFO)s
</div>'''
HTML_END = '''
</body>
</html>'''


def table_headers():
    return TABLE_HEADERS.get(LANG, TABLE_HEADERS['en_GB'])


def get_size(file):
    size = os.path.getsize(file)

    return size_text(size)


def size_text(size):
    """
    Return a nice human-readable text for the size.

    >>> print(size_text(50))
    50 bytes

    >>> print(size_text(5120))
    5.0 KB

    >>> print(size_text(5242880))
    5.0 MB
    """
    if size < 1000:
        return '%s bytes' % size

    kilo = size / 1024
    if kilo < 1000:
        return '%s KB' % round(kilo, 1)

    mega = kilo / 1024
    return '%s MB' % round(mega, 1)


def get_filetype(file_name):
    ext = os.path.splitext(file_name)[-1].lower()
    try:
        return ' %s' % FILE_TYPES[ext]
    except KeyError:
        return ''


def html_render(path, back, dirs, files, template_file=None):
    global PATH
    PATH = os.path.basename(os.path.realpath(path))

    with open(os.path.join(path, 'index.html'), 'w', encoding='utf-8') as index:
        _html_render(index, back, dirs, files, template_file=template_file)


def _html_render(index, back, dirs, files, template_file=None):
    if template_file:
        template = pathlib.Path(template_file).read_text(encoding='utf-8')
        head_start = template.find('<head>') + 6
        table_start = template.find('%(FILES)s')
        index.write(template[0:head_start] % globals())
        index.write(HTML_STYLE + HTML_JAVASCRIPT)
        index.write(template[head_start:table_start] % globals())
    else:
        index.write(HTML_START % globals())
        index.write(HTML_HEADER % PATH)

    index.write(HTML_TABLE_START % table_headers())

    if back:
        index.write(HTML_BACK)

    for file in dirs:
        file_name = os.path.basename(file)
        file_time = time.strftime(DATE_FORMAT, time.localtime(os.path.getmtime(file)))
        file_time_sort = os.path.getmtime(file)
        index.write(HTML_DIR % locals())

    dir_info = None

    for file in files:
        file_name = os.path.basename(file)
        if 'dir-info' in file_name:
            dir_info = pathlib.Path(file).read_text(encoding='utf-8')
            continue
        file_type = get_filetype(file_name)
        file_size = get_size(file)
        file_size_sort = os.path.getsize(file)
        file_time = time.strftime(DATE_FORMAT, time.localtime(os.path.getmtime(file)))
        file_time_sort = os.path.getmtime(file)
        index.write(HTML_FILE % locals())

    now = time.strftime(DATE_FORMAT, time.localtime())
    index.write(HTML_TABLE_END % (now, SCRIPT_WWW, metadata.version('dropbox-index')))

    if template_file:
        global DIR_INFO
        DIR_INFO = dir_info or ''
        index.write(template[table_start + 9 :] % globals())
        DIR_INFO = None
    else:
        index.write(HTML_DIR_INFO % {'DIR_INFO': dir_info or ''})
        index.write(HTML_END)


def crawl(path, back=None, recursive=False, template_file=None):
    """
    >>> tmp_path = getfixture('tmp_path')
    >>> crawl(tmp_path / 'foo')
    ERROR: Path ...foo does not exist

    >>> sample_dir = getfixture('sample_dir')
    >>> crawl(sample_dir / 'foo.txt')
    ERROR: Path ...foo.txt is not a directory
    """
    if not os.path.exists(path):
        print('ERROR: Path %s does not exist' % path)
        return

    if not os.path.isdir(path):
        print('ERROR: Path %s is not a directory' % path)
        return

    # get contents of the directory
    contents = [
        os.path.join(path, file)
        for file in os.listdir(path)
        if not file.endswith('index.html')
        # exclude "hidden" files
        and not file.startswith('.')
    ]

    # get only files
    files = sorted(filter(os.path.isfile, contents), key=str.lower)

    # get only directories
    dirs = sorted(filter(os.path.isdir, contents), key=str.lower) * recursive

    # render directory contents
    html_render(path, back, dirs, files, template_file)

    print('Created index.html for %s' % os.path.realpath(path))

    # crawl subdirectories
    for dir in dirs:
        crawl(dir, path, recursive, template_file)


def parser():
    """
    >>> args = parser().parse_args(['dir'])
    >>> args.path
    'dir'
    """
    epilog = '''ATTENTION:
Script will overwrite any existing index.html file(s)!
    '''

    parser = argparse.ArgumentParser(epilog=epilog)
    parser.add_argument(
        '-R',
        '--recursive',
        action='store_true',
        default=False,
        help='Include subdirectories',
    )
    parser.add_argument('-T', '--template', help='Use HTML file as template')
    parser.add_argument('path', metavar='DIRECTORY')

    return parser


def run():  # pragma: no cover
    args = parser().parse_args()
    crawl(path=args.path, recursive=args.recursive, template_file=args.template)
