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
    author_email="janisl.gutjrekl.gov, jordan.eisenman@nrel.gov",
    packages=find_namespace_packages(include=["pipes*", "pipes_sdk*", "pipes_cmd*"]),
    python_requires=">=3.8.0",
    url="https://github.com/nrel-pipes/nrel-pipes",
    install_requires=requirements,
    include_package_data=True,
    keywords="nrel pipes",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'pipes-cli=pipes_cmd.cli:main',
        ],
    },
)
