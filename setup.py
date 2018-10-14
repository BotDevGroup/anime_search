#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'marvinbot',
    'requests',
    'xmltodict'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='anime_search',
    version='0.1.0',
    description="A plugin for marvinbot to fetch anime torrents from Nyaa.si",
    long_description=readme,
    author="Albert Espinosa",
    author_email='AlbertEspinosaLeyba@Gmail.com',
    url='https://github.com/BotDevGroup/anime_search',
    packages=[
        'anime_search',
    ],
    package_dir={'anime_search':
                 'anime_search'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='anime_search',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    dependency_links=[
        'git+ssh://git@github.com:BotDevGroup/marvin.git#egg=marvinbot',
    ],
)
