#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from .error import AppError
from .lib import warn, execute


def run() -> None:
    """ Create or update dest files
    """
    try:
        execute(is_run=True)
    except AppError as e:
        warn(e)
        sys.exit(1)
