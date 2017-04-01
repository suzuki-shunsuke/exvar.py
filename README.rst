exvar
=====

|Build Status| |PyPI version|

Local repository specific application configuration management
framework.

Motivation (Background)
-----------------------

Some configurations depend on the environment where their application
runs so it is diffcult to manage them by version control system(vcs).

For example, the port number application uses depends on the
environment. To hardcode the port number in the configuration file has
trouble when the port number is used by another process.

One of the approaches to deal with this problem are to use environment
variables. There are some useful tools to manage the environment
variables (such as `direnv <https://github.com/direnv/direnv>`__). But
unfortunately many configuration files can't refer the environment
variables. In addition, it may be trivial, but many such tools doesn't
provide the template file manages the environment specific
configurations and their default values.

exvar deals with above problems.

Note that we refer to the environment variable management tools in the
above, but exvar doesn't conflict with them at all.

Why do we call exvar a "framework"?
-----------------------------------

exvar provides the consistent and generic way to manage the environment
specific configurations in the project using vcs. You don't need to be
worried about how to manage them, and don't need to develop your own
rules and tools any more.

Terms
-----

There are some exvar specific terms.

-  base file (.exvar.base.yml)
-  user file (.exvar.yml)
-  variable (placeholder)
-  source file (template)
-  destination file

base file (.exvar.base.yml)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This file should be managed by vcs. This file is required.

.. code:: yaml

    ---
    config:
      # (default source file name) = default_prefix + (destination filename) + default_suffix
      default_prefix: .
      default_suffix:
    files:
      # relative path from the directory where the base file exists
      <destination file path>:
        [src: source file's relative path from the parent directory of the base file]
        [comment: comment about the destination file]
        vars:
          # variable name format is free
          <variable name>:
            [comment: comment about the variable]
            # If the "value" field doesn't exist, the value must be set in the user file.
            # If it is null, it is treated as the empty string
            [value: the variable value]

user file (.exvar.yml)
~~~~~~~~~~~~~~~~~~~~~~

This file should not be managed by vcs. This file is not required if all
variables have default values in the base file.

.. code:: yaml

    ---
    files:
      <destination file path>:
        <variable name>:
          [comment: description about the variable's value]
          # If the "value" field doesn't exist,
          # the value must be set in the base file.
          # If the value of it is null, it is treated as the empty string
          [value: null]

variable
~~~~~~~~

variable name
^^^^^^^^^^^^^

The format of variable name is free. It is important that exvar doesn't
a template engine. exvar simply replace variable names to variable
values.

variable value
^^^^^^^^^^^^^^

The type of the variable value is string. If the type of the value of
the "value" field in the base file and user file is not scalar (such as
list or dict etc), the error will have occured. If the type of it is
int, the value is coverted to str. If it is null, it is treated as the
empty string.

source file
~~~~~~~~~~~

This file should be managed by vcs. The format of source files is free.
It is important that exvar doesn't a template engine. exvar simply
replace your defined placeholders(arbitary strings) to actual values.

destination file
~~~~~~~~~~~~~~~~

This file shouldn't be managed by vcs. This is generated automatically
by ``exvar run`` command, so you shouldn't edit this directly.

Use case 1. docker-compose.yml
------------------------------

We describe how to use exvar using a concrete use case.

In The following "docker-compose.yml" the host's port number is
hardcoded. In some case this is inconvenient.

.. code:: yaml

    # docker-compose.yml
    services:
      db:
        image: mysql
        ports: "3306:3306"

By exvar, make the source file ".tmpl.docker-compose.yml" and replace
the host's port number to the variable.

::

    $ mv docker-compose.yml .tmpl.docker-compose.yml
    $ vi .tmpl.docker-compose.yml

.. code:: yaml

    # .tmpl.docker-compose.yml (source)
    services:
      db:
        image: mysql
        ports: "$port:3306"

And create the base file and user file and edit the base file to set the
default value of the variable "$port".

::

    $ exvar init
    $ vi .exvar.base.yml

.. code:: yaml

    # .exvar.base.yml
    config:
      default_prefix: .tmpl.
      default_suffix:
    files:
      docker-compose.yml:
        vars:
          $port:
            value: 3306  # default value

If you want to set the port number to "4306" in your local repository,
set the value in the .exvar.yml .

.. code:: yaml

    # .exvar.yml
    files:
      docker-compose.yml:
        $port:
          value: 4306

You can validate the base file and user file and source file by
``exvar check`` command.

::

    $ exvar check

Finally, you can create the destination file (in this case
"docker-compose.yml") by ``exvar run`` command.

::

    $ exvar run

You should add destination files (in this case "docker-compose.yml") and
user file to .gitignore.

::

    # .gitignore
    docker-compose.yml
    .exvar.yml

Requirements
------------

-  Python 3

Install
-------

::

    $ pip install exvar

Usage
-----

::

    $ exvar -v, --version         Print the exvar version number and exit.
    $ exvar --help                Show the help message and exit.
    $ exvar init                  Create .exvar.base.yml and .exvar.yml if they don't exist.
    $ exvar check [--check-dest]  Validate the base file and user file and source files and destination files.
    $ exvar run                   Create or update dest files.
    $ exvar ls-dest               List destination file paths.
    $ exvar root-path             Print the absolute path of the parent directory of the base file.

Comparison with similar softwares
---------------------------------

Unfortunately we can't find similar softwares. Please issue if you find
them.

Contributing
------------

1. Fork (https://github.com/suzuki-shunsuke/exvar.py/fork)
2. Create a feature branch
3. Commit your changes
4. Rebase your local changes against the master branch
5. Run test suite with the ``pytest`` command and confirm that it passes
6. Create a new Pull Request

License
-------

`MIT <LICENSE>`__

Author
------

`Suzuki Shunsuke <https://github.com/suzuki-shunsuke>`__

.. |Build Status| image:: https://travis-ci.org/suzuki-shunsuke/exvar.py.svg?branch=master
   :target: https://travis-ci.org/suzuki-shunsuke/exvar.py
.. |PyPI version| image:: https://badge.fury.io/py/exvar.svg
   :target: https://badge.fury.io/py/exvar
