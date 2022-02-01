from setuptools import setup, find_packages

LONG_DESCRIPTION = open('README.md', 'r').read()

REQUIREMENTS = open('requirements-publish.txt', 'r').read().split('\n')

setup(
    name='dydx-python',
    version='0.11.3',
    packages=find_packages(),
    package_data={
        'dydx': ['abi/*.json'],
    },
    description='dYdX Python REST API for Limit Orders',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/dydxprotocol/dydx-python',
    author='dYdX Trading Inc.',
    license='Apache 2.0',
    author_email='contact@dydx.exchange',
    install_requires=REQUIREMENTS,
    keywords='dydx exchange rest api defi ethereum eth',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
