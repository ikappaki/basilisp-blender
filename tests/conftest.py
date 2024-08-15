from pathlib import Path
import pytest
import os


def pytest_addoption(parser):
    parser.addoption("--integration", action="store_true", help="Only run integration tests.")

def pytest_collection_modifyitems(config, items):
    int_path = 'tests/basilisp_blender/integration'

    if config.getoption("--integration"):
        items[:] = [item for item in items if Path(int_path).absolute() in Path(item.fspath).parents]
    else:
        items[:] = [item for item in items if Path(int_path).absolute() not in Path(item.fspath).parents]


