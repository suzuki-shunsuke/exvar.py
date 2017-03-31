#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.cnst import BASE_FILE
from src.error import AppError
from src.init import init
from src.lib import find_base, warn, execute


def test_warn():
    warn("hoge")


def test_find_base(tmpdir):
    with pytest.raises(AppError):
        find_base(tmpdir)
    with open(os.path.join(tmpdir, BASE_FILE), "w") as w:
        w.write("[")
    with pytest.raises(AppError):
        find_base(tmpdir)
    os.remove(os.path.join(tmpdir, BASE_FILE))
    os.chdir(tmpdir)
    init()
    path, data = find_base(tmpdir)
    assert path == tmpdir


def test_execute(tmpdir):
    pass
