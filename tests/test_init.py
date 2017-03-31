#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.cnst import BASE_FILE, USER_FILE
from src.init import init


def test_init(tmpdir):
    os.chdir(tmpdir)
    assert not os.path.isfile(BASE_FILE)
    assert not os.path.isfile(USER_FILE)
    init()
    assert os.path.isfile(BASE_FILE)
    assert os.path.isfile(USER_FILE)
