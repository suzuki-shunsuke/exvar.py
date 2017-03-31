#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from .error import AppError
from .lib import warn, execute


def check(check_dest) -> None:
    """ Validate the base file and user file and
    source files and destination files.
    """
    try:
        if not execute(is_check=True, is_check_dest=check_dest):
            sys.exit(1)
    except AppError as e:
        warn(e)
        sys.exit(1)
