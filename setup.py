#!/usr/bin/env python
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--strict', '--verbose', '--tb=long', 'tests']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='shopy',
    version='0.0.1',
    packages=['shopy'],
    package_data={'shopy': ['LICENSE', 'README.md']},
    url='https://github.com/MrLeeh/shopy',
    license='OSI Approved :: MIT License',
    author='Stefan Lehmann',
    author_email='stefan.st.lehmann@gmail.com',
    description='',
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=[
        'tabulate',
        'lxml',
        'requests',
        'colorama'
    ],
    platforms='any'
)
