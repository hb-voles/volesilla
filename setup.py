"""Volesilla's Setup script"""

from setuptools import setup, find_packages

setup(
    name='volesilla',
    description='CS:GO Team Dashboard',
    version='0.0.1',
    author='celestian',
    license='GPLv3',
    url='https://github.com/hb-voles/volesilla',

    packages=find_packages(),

    install_requires=[
        'docopt',
        'python-dateutil',
        'requests',
        'beautifulsoup4',
        'uWSGI==2.0.17',
        'Flask==0.12',
        'Flask-SQLAlchemy',
        'Flask-Mail==0.9.1',
        'Flask-Bootstrap==3.3.7.1',
        'wtforms',
        'Flask-WTF==0.14.2',
        'flask-bcrypt',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
