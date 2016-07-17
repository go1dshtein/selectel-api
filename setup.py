#!/usr/bin/env python
from setuptools import setup


setup(name='selectel-api',
      version='0.1.5',
      description='Simple selectel API',
      author='Kirill Goldshtein',
      author_email='goldshtein.kirill@gmail.com',
      url='https://github.com/go1dshtein/selectel-api',
      packages=['selectel'],
      install_requires=['requests >= 1.2.1'],
      license='MIT',
      classifiers=['Intended Audience :: Developers',
                   'Topic :: Software Development :: Libraries',
                   'Development Status :: 3 - Alpha',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
                   ])
