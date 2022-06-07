from setuptools import setup

version = "1.2.0"

with open("README.md") as f:
    long_description = f.read()

setup(
    name="oimdp",
    version=version,
    url="http://github.com/OpenITI/oimdp",
    author="Raff Viglianti",
    author_email="rviglian@umd.edu",
    packages=["oimdp"],
    description="OpenITI mARkdown Parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    test_suite="tests",
    python_requires=">=3.8.*",
)
