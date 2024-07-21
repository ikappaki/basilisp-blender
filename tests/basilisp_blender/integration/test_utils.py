"Integration test utils."
import os
import subprocess
import tempfile
import time

import pytest

from dev.dev_utils import blender_exec_path_get, file_exists_wait

pytestmark = pytest.mark.integration


def blender_run(*args, background=False):
    """Executes the Blender executable located using the
    `blender_exec_path_get` function, in a subprocess with the
    provided `args` command line arguments.

    It waits for the subprocess to complete and returns the result of
    `subprocess.run`, of which see.

    If the `background` keyword argument is True (default is False),
    the subprocess is run in the background with its stdin, stdout and
    stderr redirect to pipes. In this case, the function returns the
    results of `subprocess.Popen`, of which see.

    """
    bp = blender_exec_path_get()
    assert bp is not None
    cmd_args = (bp,) + args
    result = None
    if background:
        result = subprocess.Popen(
            cmd_args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    else:
        result = subprocess.run(cmd_args, capture_output=True, text=True)
    return result


def blender_eval(code):
    """Executes the Python `code` in a Blender subprocess created with
    `blender_run` and returns its result.

    """
    fd, path = tempfile.mkstemp(suffix=".py", prefix="basilisp-blender-test_")
    try:
        with os.fdopen(fd, "w") as temp_file:
            temp_file.write(code)
            temp_file.close()
        result = blender_run("--background", "--python", path)
        return result
    finally:
        os.unlink(path)


def blender_eval_file(filepath):
    """Executes the Python code located at `filepath` in a background
    Blender subprocess created with `blender_run` and returns the
    subprocess.

    """
    path = str(filepath)
    process = blender_run(
        "--factory-startup", "-noaudio", "--python", path, background=True
    )
    return process


def blender_lpy_eval(code):
    """Executes the Basilisp `code` in a Blender subprocess
    created with `blender_eval` and returns its result."""
    # force rep to be with single quotes
    code = repr(';;"\n' + code)
    py_code = f"""from basilisp_blender import eval as evl
res = evl.eval_str({code})
print(f":lpy-result {{res}}")
"""
    return blender_eval(py_code)


def test_blender_exec_path_get():
    assert blender_exec_path_get() is not None


def test_blender_run():
    result = blender_run("--version", background=False)
    assert result.stdout.startswith("Blender")


def test_blender_run_background():
    process = blender_run("--version", background=True)
    stdout, stderr = process.communicate(timeout=2)

    assert stdout.startswith("Blender")


def test_blender_eval():
    result = blender_eval('print(":result hi")')
    assert ":result hi" in result.stdout


@pytest.mark.skipif(
    os.getenv("RUNNER_OS", "Linux") != "Linux",
    reason="GHA UI test is only supported on Linux.",
)
def test_blender_eval_file(tmp_path):
    codepath = tmp_path / "blender-eval-file-test"
    sigfile = tmp_path / "blender-eval-file-test.signal"
    with open(codepath, "w") as file:
        file.write(
            f"""import sys
print(":running...")
sys.stdout.flush()
with open({repr(str(sigfile))}, "w") as file:
    file.write(":done")
    """
        )

    process = None
    try:
        process = blender_eval_file(codepath)

        file_exists_wait(sigfile, 10, 0.5)
        assert os.path.exists(str(sigfile))

        assert process.poll() is None
        process.terminate()
        out, error = process.communicate()
        assert error == ""
        assert out.startswith(":running...")
    finally:
        process.terminate()


def test_blender_lpy_eval():
    result = blender_lpy_eval("(+ 1024 1024)")
    assert ":lpy-result 2048" in result.stdout
