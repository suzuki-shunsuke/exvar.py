#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.error import AppError  # noqa: E402


def test_AppError():
    with pytest.raises(AppError):
        raise AppError()
    msg = "hello"
    try:
        raise AppError(msg)
    except AppError as e:
        assert e.message == msg
        assert str(e) == msg
