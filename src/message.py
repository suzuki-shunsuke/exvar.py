#!/usr/bin/env python
# -*- coding: utf-8 -*-

WARN_NONE_VAR = """
a var the value isn't set is found

destination file: {}
variable name: {}
""".strip()

WARN_UNUSED_VAR = """
unused variable is found

source file: {}
variable name: {}
""".strip()

WARN_DIFF_SRC_DEST = """
The content of the destination file is different from
the source text replaced variable names with variable values.
Destination files are generated automatically,
so if you add some modifications to the destination file directly,
you should add them to the source file and run `exvar run`

destination file: {}
""".strip()

WARN_UNKNOWN_VAR_EXIST = """
the variable "{}" exists in the .exvar.yml
but doesn't exist in the .exvar.base.yml

destination file: {}
variable name: {}
""".strip()

WARN_UNKNOWN_FILE_EXIST = """
the destination file "{}" exists in the .exvar.yml
but doesn't exist in the .exvar.base.yml
""".strip()

BASE_FILE_NOT_FOUND = """
.exvar.base.yml is not found
""".strip()

INVALID_BASE_CFG = """
the format of .exvar.base.yml is invalid
""".strip()

INVALID_USER_CFG = """
the format of .exvar.yml is invalid
""".strip()

INVALID_VAR = """
the variable value must be string or int or null.
""".strip()
