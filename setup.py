#!/usr/bin/python
from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        import shlex
        if self.tox_args:
            errno = tox.cmdline(args=shlex.split(self.tox_args))
        else:
            errno = tox.cmdline()
        sys.exit(errno)


setup(name='selectel-api',
      version='0.1.1',
      description='Simple selectel API',
      author='Kirill Goldshtein',
      author_email='goldshtein.kirill@gmail.com',
      url='https://github.com/go1dshtein/selectel-api',
      packages=['selectel'],
      install_requires=['requests >= 1.2.1'],
      license='GPLv2',
      tests_require=['tox', 'discover'],
      cmdclass={'test': Tox},
      classifiers=['Intended Audience :: Developers',
                   'Topic :: Software Development :: Libraries',
                   'Development Status :: 3 - Alpha',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.3'])
