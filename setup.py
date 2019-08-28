from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='oimdp',
    version='0.0.1',
    url='https://github.com/umd-mith/oimdp',
    author='Raff Viglianti',
    description='OpenITI mARkdown Parser',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Apache 2.0',
    packages=find_packages(),
)
