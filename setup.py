#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from pathlib import Path
from setuptools import find_packages, setup


ROOT_PATH = Path(__file__).parent

LICENSE_PATH = ROOT_PATH / 'LICENSE'

README_PATH = ROOT_PATH / 'README.rst'

REQUIREMENTS_PATH = ROOT_PATH / 'requirement' / 'main.txt'

REQUIREMENTS_TEST_PATH = ROOT_PATH / 'requirement' / 'test.txt'

REQUIREMENTS_RQ_PATH = ROOT_PATH / 'requirement' / 'extras-rq.txt'


def stream_requirements(fd):
    """For a given requirements file descriptor, generate lines of
    distribution requirements, ignoring comments and chained requirement
    files.

    """
    for line in fd:
        cleaned = re.sub(r'#.*$', '', line).strip()
        if cleaned and not cleaned.startswith('-r'):
            yield cleaned


with REQUIREMENTS_PATH.open() as requirements_file:
    REQUIREMENTS = list(stream_requirements(requirements_file))


with REQUIREMENTS_TEST_PATH.open() as test_requirements_file:
    REQUIREMENTS_TEST = REQUIREMENTS[:]
    REQUIREMENTS_TEST.extend(stream_requirements(test_requirements_file))

with REQUIREMENTS_RQ_PATH.open() as rq_requirements_file:
    RQ_REQUIREMENTS = list(stream_requirements(rq_requirements_file))


setup(
    name='triage',
    version='3.2.1',
    description="Risk modeling and prediction",
    long_description=README_PATH.read_text(),
    author="Center for Data Science and Public Policy",
    author_email='datascifellows@gmail.com',
    url='https://github.com/dssg/triage',
    packages=find_packages('src', exclude=['tests', 'tests.*']),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=REQUIREMENTS,
    entry_points={
        'console_scripts': ['triage = triage.cli:execute'],
    },
    extras_require={'rq': RQ_REQUIREMENTS},
    license=LICENSE_PATH.read_text(),
    zip_safe=False,
    keywords='triage',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=REQUIREMENTS_TEST,
)
