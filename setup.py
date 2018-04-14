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
        'flask-bootstrap',
        'Flask-User==0.6.19',
        'Flask-Mail',
        'Flask-Babel',
        'Flask-BabelEx',
        'Flask-WTF',
        'Flask-Nav',
        'docopt',
        'uwsgi',
        'pylint',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
