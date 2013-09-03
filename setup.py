#!/usr/bin/env python

from setuptools import setup, find_packages

import dropbox_index


setup_params = dict(
    name='dropbox-index',
    version=dropbox_index.__version__,
    author="Wojciech 'KosciaK' Pietrzok",
    author_email='kosciak@kosciak.net',
    description='Creates index.html for directory contents shared publicly on Dropbox. That way you can easily share whole content of the directory without the need to send separate links for all the shared files',
    long_description='Visit project\s page for details.',
    url='http://code.google.com/p/kosciak-misc/wiki/DropboxIndex',
    license='Apache License v2',
    keywords='dropbox',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License",
    ],
    packages=find_packages(exclude=['ez_setup',
                                    'tests', 'tests.*'
                                    'examples', 'examples.*']),
    entry_points={
        'console_scripts': [
            'dropbox-index = dropbox_index:run',
        ],
    },
)

if __name__ == '__main__':
    setup(**setup_params)
