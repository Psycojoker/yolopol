# -*- coding: utf-8 -*-

"""
This file registers a django system check to ensure 3rd party browser libraries
are available.

Each needed library is declared below in dict GITHUB_LIBS, with the expected
static/libs subdirectory name for the library as a key.  Each library has the
following keys:
- 'repo': repository name on github ('user-or-org/repo-name')
- 'ref': git refname to download (ie. tag, branch, commit...)
- 'check': relative path to a file that indicates the library is there

When running, the checking code loops over libraries, checks if the expected
file is present, and if not tries to download it from GitHub.  If that's
successful, it issues an 'Info' CheckMessage ; if there's a download error or
the expected file is still missing, an 'Error' CheckMessage is issued.
"""

import os
import shutil
import sys
import urllib
from zipfile import ZipFile

from django.core.checks import Info, Error

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)
)))
LIBS_DIR = os.path.join(BASE_DIR, 'static/libs')
GITHUB_LIBS = {
    'jquery': {
        'repo': 'jquery/jquery',
        'ref': '2.1.4',
        'check': 'dist/jquery.min.js'
    },

    'fontawesome': {
        'repo': 'FortAwesome/Font-Awesome',
        'ref': 'v4.3.0',
        'check': 'css/font-awesome.min.css'
    },

    'flag-icon-css': {
        'repo': 'lipis/flag-icon-css',
        'ref': '0.7.1',
        'check': 'css/flag-icon.min.css'
    },

    'bootstrap': {
        'repo': 'twbs/bootstrap',
        'ref': 'v3.3.5',
        'check': 'dist/js/bootstrap.min.js'
    }
}


def get_from_github(repo, ref, destination):
    # Remove destination directory if present
    if os.path.isdir(destination):
        shutil.rmtree(destination)

    # Ensure parent exists
    parent = os.path.dirname(destination)
    if not os.path.isdir(parent):
        os.makedirs(parent)

    # Download to {destination}.zip
    zip_path = '%s.zip' % destination
    urllib.urlretrieve(
        'https://github.com/%s/archive/%s.zip' % (repo, ref), zip_path
    )

    with ZipFile(zip_path) as z:
        # Get base directory name inside zipfile
        zip_base = os.path.join(parent, z.namelist()[0])

        # Extract zipfile
        z.extractall(parent)

        # Move extracted directory to destination
        os.rename(zip_base, destination)

    # Unlink zipfile
    os.remove(zip_path)


def libs_check(app_configs, **kwargs):
    """
    Checks for the presence of browser libraries and tries to download them
    """
    messages = []

    for dirname, options in GITHUB_LIBS.items():
        fulldir = os.path.join(LIBS_DIR, dirname)
        check = os.path.join(fulldir, options['check'])

        if not os.path.isfile(check):
            descr = '%(repo)s (%(ref)s) from GitHub' % options

            print >>sys.stderr, 'Missing %s, downloading %s' % (dirname, descr)

            try:
                get_from_github(options['repo'], options['ref'], fulldir)
            except Exception as e:
                messages.append(Error(
                    'Error downloading %s' % descr,
                    hint=str(e),
                    id='checks.E002'
                ))
            else:
                if os.path.isfile(check):
                    messages.append(Info(
                        'Library %s was missing, downloaded %s' %
                        (dirname, descr),
                        id='checks.I001'
                    ))
                else:
                    messages.append(Error(
                        'Cannot find file %s after downloading %s' %
                        (options['check'], descr),
                        hint='File was expected at %s' % check,
                        id='checks.E003'
                    ))

    return messages
