# -*- coding:utf-8 -*-
from setuptools import find_packages, setup

setup(
    name="jav_scraper",
    version="0.0.1",
    packages=find_packages(),
    author='LibertX',
    author_email='libertx@ltsp.fr',
    description="LTSP Tools",
    install_requires=[
        "setuptools"
        "bs4",
        "sqlalchemy"
    ]
)
