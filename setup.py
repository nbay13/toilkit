from setuptools import setup, find_packages

setup(
    name='toilkit',
    version='0.1',
    description='A command-line tool for processing genomic data',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'biopython'
    ],
    entry_points={
        'console_scripts': [
            'toilkit = toilkit.cli:main',
        ],
    },
)
