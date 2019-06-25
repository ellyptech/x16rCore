#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup

def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


# Get the long description from the relevant file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(name='pyhdl',
      version='0.0.1',
      description=u"Skeleton of a Python package",
      long_description=long_description,
      classifiers=[],
      keywords='',
      author=u"Abhishek Bajpai",
      author_email='abhvajpayee@gmail.com',
      url='https://github.com/abhvajpayee/phdl',
      license='Apache',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
      include_package_data=True,
      zip_safe=False,
      install_requires=read('requirements.txt').splitlines(),
      setup_requires=["pytest-runner",],
      tests_require=["pytest",],
      #entry_points="""
      #[console_scripts]
      #pyskel_bc=pyskel_bc.cli:cli
      #"""
      )
