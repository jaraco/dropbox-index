.. image:: https://img.shields.io/pypi/v/dropbox-index.svg
   :target: https://pypi.org/project/dropbox-index

.. image:: https://img.shields.io/pypi/pyversions/dropbox-index.svg

.. image:: https://github.com/jaraco/dropbox-index/workflows/tests/badge.svg
   :target: https://github.com/jaraco/dropbox-index/actions?query=workflow%3A%22tests%22
   :alt: tests

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Ruff

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: Black

.. .. image:: https://readthedocs.org/projects/PROJECT_RTD/badge/?version=latest
..    :target: https://PROJECT_RTD.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/badge/skeleton-2023-informational
   :target: https://blog.jaraco.com/skeleton

Introduction

Creates index.html for directory contents shared publicly on Dropbox. That way you can easily share whole content of the directory without the need to send separate links for all the shared files.
Download

Check the Downloads section, install using pip / easy_install from PyPI, or checkout the source from Subversion repository using svn checkout http://kosciak-misc.googlecode.com/svn/python/dropbox-index/trunk/ dropbox-index
Requirements

Script was tested on Linux but should work on all operating systems with Python <= 2.6 installed. Users have informed that it runs on Windows with Activestate's ActivePython 2.6 and on MacOSX.

Generated index.html pages were tested on Linux with Chrome 4.x, Firefox 3.0.x, and Opera 10.x
Installation

Download, extract, and run: python setup.py install
Usage

Just run this Python script with directory as an argument (and add -R as an option if you want to include subdirectories) ``` Usage: dropbox-index [options] DIRECTORY

Options: --version show program's version number and exit -h, --help show this help message and exit -R, --recursive Include subdirectories [default: False] -T TEMPLATE, --template=TEMPLATE Use HTML file as template

ATTENTION: Script will overwrite any existing index.html file(s)!

Example: ./dropbox-index.py -R -T template.html ~/Dropbox/Public/show ``` Script will generate index.html for directory (and subdirectories if run in recursive mode). Hidden files on Linux (filename starting with '.') are automatically omited.

If a directory contains a file with dir-info in it's name (dir-name, dir-name.txt, dir-name.html, - all these names are valid) the contents of the file will be used in the index.html as and additional information about directory content.

From version 0.4 you can click on the table's headings to sort files by name, size, or date (in ascending and descending order).

ATTENTION! Script will overwrite any existing index.html file without asking for permission!
Template

Templates can be used to generate custom index.html files. Selected template is uded to generate all pages, including subdirectories if the script is run i recursive mode.

Templates are just regular HTML files. CSS styles and JavaScript code will be automatically inject. The table with the files list will be injected in place of %(FILES)s

You can use (names are case sensitive!): * %(FILES)s - must be included or the files list won't be injected! * %(FAVICON)s - place it inside <head> if you want Dropbox-favicon to be used * %(ENCODING)s - system encoding identified by the script * %(PATH)s - name of the directory * %(DIR_INFO)s - place for additional directory information (from dir-info files
Screenshot

Just check the shared folder containing icons and screenshot:

Icons

I have used icons from famfamfam's "Silk" icon set
Authors

    Wojciech 'KosciaK' Pietrzok
    Tommy MacWilliam - introduced template system
