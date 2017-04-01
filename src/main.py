#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from pkg_resources import resource_string

import click

from .check import check
from .init import init
from .ls_dest import ls_dest
from .root_path import root_path
from .run import run

if __name__ == "__main__":
    VERSION = json.loads(
        resource_string(__name__, "../package.json"))["version"]
else:
    VERSION = json.loads(resource_string("exvar", "package.json"))["version"]


@click.group(invoke_without_command=True)
@click.pass_context
@click.option("--version", "-v", is_flag=True,
              help="Print the exvar version number and exit")
def cmd(ctx, version):
    if ctx.invoked_subcommand is None:
        if version:
            click.echo(VERSION)
        else:
            click.echo(ctx.get_help())


cmd.command()(init)
click.option(
    "--check-dest", is_flag=True, help="check the dest file")(check)
cmd.command()(check)
cmd.command()(run)
cmd.command("ls-dest")(ls_dest)
cmd.command("root-path")(root_path)


def main():
    cmd(obj={})


if __name__ == '__main__':
    main()
