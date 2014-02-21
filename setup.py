#!/usr/bin/python2.7

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='selectel-api',
      version='0.1',
      description='Simple selectel API',
      author='Kirill Goldshtein',
      author_email='goldshtein.kirill@gmail.com',
      url='https://github.com/go1dshtein/selectel-api',
      packages=['selectel'],
      requires=['requests'],
      install_requires=['requests'],
      license='GPLv2',
      test_suite='tests',
      classifiers=['Intended Audience :: Developers',
                   'Topic :: Software Development :: Libraries',
                   'Development Status :: 3 - Alpha',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2.7'])
