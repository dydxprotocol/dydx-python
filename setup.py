from setuptools import setup, find_packages

LONG_DESCRIPTION = open('README.md', 'r').read()

REQUIREMENTS = [
    'requests==2.22.0',
    'requests-mock==1.6.0',
    'six==1.12',
    'web3==5.0.0',
    'eth-account==0.4.0',
    'pytest>=4.4.0,<5.0.0',
    'tox==3.13.2',
    'setuptools==41.0.1',
    'eth_keys'
]

setup(
    name='dydx-python',
    version='0.8.1',
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
