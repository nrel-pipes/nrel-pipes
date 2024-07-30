from setuptools import setup, find_namespace_packages

__version__ = "0.0.1"


requirements = [
    "requests"
]

setup(
    name="nrel-pipes",
    description="A Python package for NREL PIPES developers",
    version=__version__,
    author="NREL",
    author_email=["jianli.gu@nrel.gov", "jordan.eisenman@nrel.gov"],
    packages=find_namespace_packages(include=["nrel-pipes.pipes", "nrel-pipes.pipes_sdk"]),
    python_requires=">=3.8",
    url="https://github.com/nrel-pipes/nrel-pipes",
    install_requires=requirements,
    include_package_data=True,
    keywords="nrel,pipes"
)
