#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import click

from .error import AppError
from .lib import warn, find_base


def root_path() -> None:
    """ Print the absolute path of the parent directory of the base file.
    """
    try:
        click.echo(find_base(os.getcwd())[0])
    except AppError as e:
        warn(e)
        sys.exit(1)
