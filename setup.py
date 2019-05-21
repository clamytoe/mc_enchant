"""
setup.py

Setup for installing the package.
"""
from setuptools import setup, find_packages
from os import path
from io import open

import mc_enchant

VERSION = mc_enchant.__version__
AUTHOR = mc_enchant.__author__
EMAIL = mc_enchant.__email__

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="mc_enchant",
    version=VERSION,
    description="Little utility to facilitate with generating the code needed to spawn enchanted objects in Minecraft (mc_enchant)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/clamytoe/mc_enchant",
    author=AUTHOR,
    author_email=EMAIL,
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        # How mature is this project? Common values are
        #   1 - Planning
        #   2 - Pre-Alpha
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        #   6 - Mature
        #   7 - Inactive
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="python utility",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    install_requires=["pytest"],
    license="MIT",
    entry_points={
        "console_scripts": [
            "mc_enchant=mc_enchant.app:main"
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/clamytoe/mc_enchant/issues',
        'Source': 'https://github.com/clamytoe/mc_enchant/',
    },
)
