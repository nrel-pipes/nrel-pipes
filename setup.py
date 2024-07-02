from setuptools import setup, find_namespace_packages

__version__ = "0.0.1"

def read_requirements():
    with open('requirements.txt') as req_file:
        return req_file.read().splitlines()


setup(
    name="p",
    description="A Python package for NREL PIPES developers",
    version=__version__,
    author="NREL",
    author_email="janisl.gutjrekl.gov, jordan.eisenman@nrel.gov",
    packages=find_namespace_packages(include=["p", "p.*"]),
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
            'p=p.cli:main',
        ],
    },
)
