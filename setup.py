try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='mazerunner',
    description='A behavior implemented for NAO Robot on V-REP environment.',
    long_description=open('README.md').read(),
    version='0.1',
    packages=['mazerunner'],
    scripts=[],
    author='Lucas David',
    author_email='lucasolivdavid@gmail.com',

    url='https://github.com/lucasdavid/mazerunner',
    download_url='https://github.com/lucasdavid/mazerunner/archive/master.zip',
    install_requires=['enum', 'numpy'],
    tests_require=open('requirements-dev.txt').readlines(),
)
