from setuptools import setup, find_packages

__version__ = "0.0.1"

def read_requirements():
    with open('requirements.txt') as req_file:
        return req_file.read().splitlines()

setup(
    name="nrel-pipes",
    description="A Python package for NREL PIPES developers",
    version=__version__,
    author="NREL",
    author_email="janisl.gu@nrel.gov, jordan.eisenman@nrel.gov",
    packages=find_packages(include=["nrel_pipes", "nrel_pipes.sdk", "nrel_pipes.sdk.*"]),
    python_requires=">=3.8.0",
    url="https://github.com/nrel-pipes/nrel-pipes",
    install_requires=read_requirements(),
    include_package_data=True,
    keywords="nrel pipes",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'nrel-pipes=nrel_pipes:main',
            'pipes-sdk=nrel_pipes.sdk:main',  # Entry point for the SDK
        ],
    },
)
