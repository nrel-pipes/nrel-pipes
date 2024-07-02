"""
Top-level package for pipes.
"""
import os
from pipes_cmd.config import common

__author__ = "NREL"
__version__ = "0.1.0"

PIPES_CONFIG_DIRECTORY = common.PIPES_CONFIG_DIRECTORY

os.makedirs(PIPES_CONFIG_DIRECTORY, exist_ok=True)

