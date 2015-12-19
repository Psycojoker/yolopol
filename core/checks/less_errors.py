# -*- coding: utf-8 -*-

"""
This file declares a django system check to ensure LESS stylesheets can be
compiled without errors or warnings.  All *.less files under static/less are
checked.

Note that the check code changes directory to ensure @import directives work
as expected.  The initial cwd is restored upon completion.
"""

import lesscpy
import os

from django.core.checks import Error

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)
)))
LESS_DIR = os.path.join(BASE_DIR, 'static/less')


def less_check(app_configs, **kwargs):
    messages = []
    cwd = os.getcwd()

    for root, dirs, files in os.walk(LESS_DIR):
        os.chdir(root)
        for name in [f for f in files if f.endswith('.less')]:
            less_file_path = os.path.join(root, name)

            try:
                lesscpy.compile(less_file_path)
            except Exception as e:
                messages.append(Error(
                    'LESS compilation error on %s' %
                    os.path.relpath(less_file_path, LESS_DIR),
                    hint=str(e),
                    id='checks.E001'
                ))

    os.chdir(cwd)
    return messages
