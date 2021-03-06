from setuptools import setup, find_packages
import re
import os

setup(
    name='app',
    version='0.1',
    description='url_shortener',
    long_description='url_shortener',
    keywords='url_shortener',
    author='Jose Pedro',
    packages=find_packages(),
    include_package_data=False,
    entry_points={'console_scripts': [
        'app = app.url_shortener.url_shortener:main',]
        },
    install_requires=['flask','nose','flask-sqlalchemy','marshmallow-sqlalchemy','flask_marshmallow', 
    'marshmallow-jsonschema', 'sqlalchemy-utils'],
    test_suite='nose.collector'
        )
