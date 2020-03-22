from setuptools import setup, find_packages

__version__ = '1.0.0'


setup(
    name='meowody',
    version=__version__,
    license='BSD',
    packages=find_packages(exclude=['example', 'tests', 'docs', 'scripts']),
    zip_safe=False,
    description='',
    long_description=__doc__,
    author='xihao.liang',
    author_email='',
    install_requires=['commandr', ],
    tests_require=[],
    platforms='any',
    entry_points={}
)
