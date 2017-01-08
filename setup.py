#!/usr/bin/env python

from setuptools import setup, find_packages
import os

__version__ = '0.4'

PACKAGE_DIR = os.path.abspath(os.path.dirname(__file__))
os.chdir(PACKAGE_DIR)


setup(name='django-pint',
      version=__version__,
      url='https://github.com/bharling/django-pint',
      author="Ben Harling",
      author_email="blrharling@gmail.com",
      description=("Quantity Field for Django using pint library "
                   "for automated unit conversions"),
      long_description=open(os.path.join(PACKAGE_DIR, 'README.md')).read(),
      license='MIT',
      packages=find_packages(exclude=["sandbox*", "tests*"]),
      include_package_data=True,
      install_requires=[
          'django>=1.8',
          'pint>=0.7.2',
          ],
      # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: Unix',
                   'Programming Language :: Python']
      )
