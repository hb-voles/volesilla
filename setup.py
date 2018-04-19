'''Volesilla's Setup script'''

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
        'Flask==0.12',
        'Flask-Bootstrap==3.3.7.1',
        'Flask-User==0.6.19',
        'Flask-Mail==0.9.1',
        'Flask-Babel==0.11.2',
        'Flask-BabelEx==0.9.3',
        'Flask-WTF==0.14.2',
        'Flask-Nav',
        'docopt',
        'uWSGI==2.0.17',
        'pylint',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
