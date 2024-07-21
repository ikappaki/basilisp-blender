"""Initialize the Basilisp runtime environment."""

import logging

from basilisp import main as basilisp
from basilisp.lang import compiler

COMPILER_OPTS = compiler.compiler_opts()
basilisp.init(COMPILER_OPTS)

LOGGER = logging.getLogger("basilisp-blender")
LOGGER.addHandler(logging.StreamHandler())


def log_level_set(level, filepath=None):
    """Sets the logger in the `LOGGER` global variable to the
    specified `level`.

    If an optional `filepath` is provided, logging will also be
    written to that file.

    """
    LOGGER.setLevel(level)
    if filepath:
        file_handler = logging.FileHandler(filepath, mode="w")
        LOGGER.addHandler(file_handler)


# log_level_set(logging.DEBUG, "basilisp-blender.log")
