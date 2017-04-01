#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys

import yaml

from .cnst import BASE_FILE, USER_FILE
from .error import (
    BaseFileNotFoundError, InvalidBaseCfgError,
    InvalidUserCfgError, InvalidVarError)
from .message import (
    WARN_NONE_VAR, WARN_UNUSED_VAR, WARN_DIFF_SRC_DEST,
    WARN_UNKNOWN_FILE_EXIST, WARN_UNKNOWN_VAR_EXIST, INVALID_BASE_CFG,
    INVALID_USER_CFG)


def warn(msg) -> None:
    sys.stderr.write("[exvar][Warning] {}\n".format(msg))


def find_base(cwd: str):
    while True:
        try:
            base_cfg_path = os.path.join(cwd, BASE_FILE)
            with open(base_cfg_path) as r:
                return (cwd, r.read())
        except FileNotFoundError:
            if cwd == "/":
                raise BaseFileNotFoundError()
            cwd = os.path.dirname(cwd)


def get_str(value) -> str:
    if value is None:
        return ""
    elif isinstance(value, (str, int)):
        return str(value)
    else:
        raise InvalidVarError()


def execute(is_run=False, is_check=False, is_check_dest=False) -> bool:
    """
    """
    result = True
    pardir, base_txt = find_base(os.getcwd())
    base_cfg = validate_base_text(base_txt)
    if "config" not in base_cfg:
        raise InvalidBaseCfgError()
    if "default_prefix" not in base_cfg["config"]:
        raise InvalidBaseCfgError()
    if "default_suffix" not in base_cfg["config"]:
        raise InvalidBaseCfgError()
    default_prefix = base_cfg["config"].get("default_prefix")
    default_suffix = base_cfg["config"].get("default_suffix")
    if default_prefix is None:
        default_prefix = ""
    if default_suffix is None:
        default_suffix = ""
    try:
        with open(os.path.join(pardir, USER_FILE)) as r:
            user_cfg = yaml.load(r.read())
    except FileNotFoundError:
        # user config file is not found
        user_cfg = {"files": {}}
    except yaml.parser.ParserError as e:
        raise InvalidUserCfgError("{}\n{}".format(INVALID_USER_CFG, e))
    if not isinstance(user_cfg, dict):
        raise InvalidUserCfgError()
    if "files" not in user_cfg:
        raise InvalidUserCfgError()
    user_files = user_cfg["files"]
    if user_files is None:
        user_files = {}
    elif not isinstance(user_files, dict):
        raise InvalidUserCfgError()
    base_files = validate_base_files(base_cfg["files"])
    for dest, base_file in base_files.items():
        user_file = user_files.get(dest, {})
        if not isinstance(user_file, dict):
            raise InvalidUserCfgError()
        src = base_file.get("src", "{}{}{}".format(
            default_prefix, dest, default_suffix))
        src_path = os.path.join(pardir, src)
        try:
            with open(src_path) as r:
                src_text = r.read()
        except FileNotFoundError:
            # source file is not found
            warn("can't read {}".format(src_path))
            result = False
            continue
        for var_name, base_var in base_file.get("vars", {}).items():
            if var_name in user_file:
                user_var = user_file[var_name]
                if "value" in user_var:
                    value = get_str(user_var["value"])
                else:
                    if "value" in base_var:
                        value = get_str(base_var["value"])
                    else:
                        warn(WARN_NONE_VAR.format(dest, var_name))
                        result = False
                        continue
            else:
                if "value" in base_var:
                    value = get_str(base_var["value"])
                else:
                    warn(WARN_NONE_VAR.format(dest, var_name))
                    result = False
                    continue
            new_text = src_text.replace(var_name, value)
            if is_check and src_text == new_text:
                # the var is not used
                warn(WARN_UNUSED_VAR.format(src_path, var_name))
                result = False
                continue
            src_text = new_text
        if is_check_dest:
            try:
                with open(os.path.join(pardir, dest)) as r:
                    dest_text = r.read()
                if src_text != dest_text:
                    # warning when check command
                    warn(WARN_DIFF_SRC_DEST.format(dest))
                    result = False
                    if is_run:
                        with open(os.path.join(pardir, dest), "w") as w:
                            w.write(src_text)
            except FileNotFoundError:
                # dest file is not found
                if is_run:
                    with open(os.path.join(pardir, dest), "w") as w:
                        w.write(src_text)
        else:
            if is_run:
                with open(os.path.join(pardir, dest), "w") as w:
                    w.write(src_text)
        if is_check:
            for var_name, user_var in user_file.items():
                if var_name not in base_files:
                    warn(WARN_UNKNOWN_VAR_EXIST.format(
                        var_name, dest, var_name))
                    result = False
    if is_check:
        for dest, user_file in user_files.items():
            if dest not in base_files:
                # unknown src exists in user config
                warn(WARN_UNKNOWN_FILE_EXIST.format(dest))
                result = False
    return result


def validate_base_text(text):
    try:
        base_cfg = yaml.load(text)
    except yaml.parser.ParserError as e:
        raise InvalidBaseCfgError("{}\n{}".format(INVALID_BASE_CFG, e))
    if not isinstance(base_cfg, dict):
        raise InvalidBaseCfgError()
    if "files" not in base_cfg:
        raise InvalidBaseCfgError()
    return base_cfg


def validate_base_files(base_files):
    if base_files is None:
        return {}
    elif not isinstance(base_files, dict):
        raise InvalidBaseCfgError()
    return base_files
