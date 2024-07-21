import os
import tempfile
from pathlib import Path

import pytest

from basilisp_blender import eval as evl


@pytest.mark.parametrize(
    "r,code",
    [
        (3, "(+ 1 2)"),
    ],
)
def test_eval_str(r, code: str):
    assert r == evl.eval_str(code)


@pytest.mark.parametrize(
    "result,code",
    [
        (":result 7", "(+ 4 3)"),
    ],
)
def test_eval_file(capsys, result, code):
    temp = tempfile.NamedTemporaryFile(
        delete=False, prefix="basilispblendertest", mode="w"
    )
    try:
        temp.write(f'(import sys)(.write sys/stdout (str :result " " {code}))')
        temp.close()
        evl.eval_file(Path(temp.name).as_posix())
        captured = capsys.readouterr()
        assert captured.out == result
    finally:
        os.remove(temp.name)
