# Copyright openbkn.ai
#
# Licensed under the OpenBKN License.
# See LICENSE-OPENBKN.txt in the project root.

"""Setup Script for DBUtilsX"""

import warnings
import os
import shutil
from sys import version_info

from setuptools import setup


py_version = version_info[:2]
if not (3, 12) <= py_version < (4, 0):
    raise ImportError("Python %d.%d is not supported by DBUtils." % py_version)

warnings.filterwarnings("ignore", "Unknown distribution option")

__version__ = "0.0.1"

readme = open("README.md").read()

setup(
    name="bkn-comm-py",
    version=__version__,
    description="RDS DB API 2.0 driver with DBUtils support",
    project_urls={
        "Source Code": "https://github.com/openbkn-ai/bkn-comm-py"
    },
    platforms=["x86_64", "aarch64"],
    license="MIT License",
    packages=[
        "dbutilsx",
        "dbutilsx.dbutils",
        "rdsdriver",
        "rdsdriver.dm",
        "rdsdriver.mysql",
        "rdsdriver.kingbase",
    ],
    python_requires=">=3.12, <4",
    zip_safe=False,
    install_requires=[
        "pymysql[rsa]>=1.2.0",
        "dmPython>=2.5.32",
        "ksycopg2>=2.9.1",
    ],
)

if os.path.exists("./build"):
    shutil.rmtree("./build")
if os.path.exists("./bkn-comm-py.egg-info"):
    shutil.rmtree("./bkn-comm-py.egg-info")
