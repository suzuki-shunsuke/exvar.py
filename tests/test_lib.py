#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.cnst import BASE_FILE  # noqa: E402
from src.error import AppError  # noqa: E402
from src.init import init  # noqa: E402
from src.lib import find_base, warn  # noqa: E402


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
