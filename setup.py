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
      url='http://goldshtein.org',
      packages=['selectel'],
      requires=['requests'],
      install_requires=['requests'],
      license='GPLv2',
      #test_suite='tests',
      classifiers=['Intended Audience :: Developers',
                   'Environment :: Console',
                   'Programming Language :: Python',
                   'Development Status :: 3 - Alpha'])
