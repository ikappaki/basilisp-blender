"""Initialize the Basilisp runtime environment."""

import importlib
import logging

from basilisp import main as basilisp
from basilisp.lang import compiler
from basilisp.lang.keyword import Keyword
from basilisp.lang.util import munge

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

def control_panel_create():
    """Initialises and displays the nREPL server UI control panel. It
    returns a function to destroy the panel and settings, and stop the
    server if it is running.

    """
    ctrl_panel_mod = importlib.import_module(munge("basilisp-blender.control-panel"))
    panel = ctrl_panel_mod.nrepl_control_panel_create__BANG__()
    return panel[Keyword("destroy!")]


