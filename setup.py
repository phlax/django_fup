#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup


setup(
    name='django-fup',
    version='0.0.1',
    description='Grid row layout for Django',
    author='Ryan Northey',
    author_email='ryan@space23.net',
    long_description=open('README.md', 'r').read(),
    packages=[
        'django_fup'],
    package_data={
        'django_fup': [
            'static/django_fup/js/*',            
            'static/django_fup/css/*']},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPL License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
    zip_safe=False,
)
