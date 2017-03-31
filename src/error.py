#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .message import (BASE_FILE_NOT_FOUND, INVALID_BASE_CFG, INVALID_USER_CFG,
                      INVALID_VAR)


class AppError(Exception):
    def __init__(self, msg=None):
        if msg is not None:
            self.message = msg

    def __str__(self):
        return self.message


class BaseFileNotFoundError(AppError):
    message = BASE_FILE_NOT_FOUND


class InvalidBaseCfgError(AppError):
    message = INVALID_BASE_CFG


class InvalidUserCfgError(AppError):
    message = INVALID_USER_CFG


class InvalidVarError(AppError):
    message = INVALID_VAR
