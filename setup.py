# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='flashcard_kanji',
    version='0.1.0',
    description='Kanji flash card for everyday practice',
    long_description=readme,
    author='Evan Hutomo',
    author_email='evanhutomo@gmail.com',
    url='https://github.com/evanhutomo/flashcard_kanji',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)