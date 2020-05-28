#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import neo

# def calculate_version():
#     initpy = open("neo/_version.py").read().split("\n")
#     version = list(filter(lambda x: "__version__" in x, initpy))[0].split("'")[1]
#     return version


package_version = neo.__version__
setup(
    name="neo",
    version=package_version,
    author="Ved",
    author_email="vpved93@gmail.com",
    packages=find_packages(),
    url="https://github.com/ved93/neo",
    license="License :: OSI Approved :: MIT License",
    entry_points={"console_scripts": ["datacleaner=datacleaner:main"]},
    description=("A Python library for day to day data analysis and machine learning."),
    long_description="""
A Python library for day to day data analysis and machine learning.""",
)
