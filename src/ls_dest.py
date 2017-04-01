#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import click

from .error import AppError
from .lib import warn, find_base, validate_base_files


def ls_dest() -> None:
    """ List destination files
    """
    try:
        _, base_cfg = find_base(os.getcwd())
        click.echo("\n".join(validate_base_files(base_cfg["files"]).keys()))
    except AppError as e:
        warn(e)
        sys.exit(1)
