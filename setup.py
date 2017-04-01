import json
import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), "package.json")) as r:
    data = json.load(r)

with open(os.path.join(os.path.dirname(__file__), "README.rst")) as r:
    LONG_DESCRIPTION = r.read()

setup(
    name="exvar",
    version=data["version"],

    packages=["exvar", "exvar.src"],
    package_dir={
        "exvar": ".",
        "exvar.src": "src",
    },
    package_data={
        "exvar": ["package.json"],
        "exvar.src": ["exvar.base.yml", "exvar.yml"],
    },
    install_requires=["click", "pyyaml"],
    zip_safe=True,
    entry_points={
        "console_scripts": ["exvar=exvar.src.main:main"],
    },

    description=data["description"],
    long_description=LONG_DESCRIPTION,
    url=data["repository"],
    license=data["license"],
    author="Suzuki Shunsuke",
    author_email="suzuki.shunsuke.1989@gmail.com"
)
