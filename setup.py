# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from setuptools import setup

try:
    with open('README.rst') as f:
        readme = f.read()
except IOError:
    readme = ''

setup(
    name="Flask-Memcached",
    version='0.0.1',
    py_modules=['flask_memcached'],
    author='INADA Naoki',
    author_email='songofacandy at gmail dot com',
    url='https://github.com/KLab/Flask-Memcached',
    description="python-memcached integration for Flask",
    long_description=readme,
    install_requires=["Flask", "python-memcached>=1.50"],
)
