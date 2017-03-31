#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil

from .cnst import BASE_FILE, USER_FILE, BASE_TMPL, USER_TMPL


def _init(dirname: str, src: str, dest: str) -> None:
    if not os.path.lexists(dest):
        shutil.copyfile(os.path.normpath(os.path.join(dirname, src)), dest)


def init() -> None:
    """ Create .exvar.base.yml and .exvar.yml
    """
    dirname = os.path.dirname(__file__)
    _init(dirname, BASE_TMPL, BASE_FILE)
    _init(dirname, USER_TMPL, USER_FILE)
