#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 Gora Khargosh <gora.khargosh@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sys
import imp

from os.path import join as path_join, dirname
from setuptools import setup, find_packages
from setuptools.extension import Extension
from setuptools.command.build_ext import build_ext
from distutils.util import get_platform

version = imp.load_source('version', path_join('watchdog', 'version.py'))

def read_file(filename):
    """Reads the contents of a given file and returns it."""
    return open(path_join(dirname(__file__), filename)).read()

PLATFORM_LINUX = 'linux'
PLATFORM_WINDOWS = 'windows'
PLATFORM_MACOSX = 'macosx'

# Determine platform to pick the implementation.
platform = get_platform()
if platform.startswith('macosx'):
    platform = PLATFORM_MACOSX
elif platform.startswith('linux'):
    platform = PLATFORM_LINUX
elif platform.startswith('win'):
    platform = PLATFORM_WINDOWS
else:
    platform = None

trove_classifiers = (
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: POSIX :: Linux',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows :: Windows NT/2000',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: C',
    'Topic :: Software Development :: Libraries',
    'Topic :: System :: Monitoring',
)

ext_modules = {
    PLATFORM_MACOSX: [
        Extension(name='_watchdog_fsevents',
                  sources=['watchdog/_watchdog_fsevents.c'],
                  extra_link_args=['-framework', 'CoreFoundation',
                                   '-framework', 'CoreServices'],
                  ),
    ],
    PLATFORM_LINUX: [],
    PLATFORM_WINDOWS: [],
}

common_install_requires = ['PyYAML >= 3.09', 'argh >= 0.6.0']
if sys.version_info < (2, 6, 0):
    # Python 2.5 and below don't have the kqueue implementation in the
    # select module. This backported patch adds it.
    common_install_requires.append('select26')

install_requires = {
    PLATFORM_MACOSX: [],
    PLATFORM_LINUX: ['pyinotify >= 0.9.1'],
    PLATFORM_WINDOWS: ['pywin32 >= 214'],
}

scripts = [
    'watchmedo',
    ]

if platform == PLATFORM_WINDOWS:
    scripts.append('watchmedo.bat')

setup(
    name="watchdog",
    version=version.VERSION_STRING,
    description="Filesystem events monitoring",
    long_description=read_file('README.md'),
    author="Gora Khargosh",
    author_email="gora.khargosh@gmail.com",
    license="MIT License",
    cmdclass=dict(build_ext=build_ext),
    url="http://github.com/gorakhargosh/watchdog",
    download_url="http://watchdog-python.googlecode.com/files/watchdog-%s.tar.gz" % version.VERSION_STRING,
    keywords = "python filesystem monitoring monitor fsevents inotify",
    classifiers=trove_classifiers,
    ext_modules=ext_modules.get(platform, []),
    packages=find_packages(),
    scripts=scripts,
    zip_safe=False,
    install_requires=common_install_requires + install_requires.get(platform, []),
    )
