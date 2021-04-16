#!/usr/bin/env python
import os
from setuptools import setup, find_packages

root_dir = os.path.abspath(os.path.dirname(__file__))
readme = open(os.path.join(root_dir, 'README.md')).read()
requirements = [
    name.rstrip()
    for name in open(os.path.join(root_dir, 'requirements.txt')).readlines()
]
version = open(os.path.join(root_dir, 'VERSION')).read().strip()

setup(
    name='autowebprint',
    version=version,
    author='CreeperLin',
    author_email='linyunfeng@sjtu.edu.cn',
    url='https://github.com/CreeperLin/autowebprint',
    description='Automatically printing web pages (to PDF) using browsers and selenium in Python.',
    long_description=readme,
    packages=find_packages(exclude=('test')),
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5',
)
