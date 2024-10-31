"Integration test utils."
import os
import subprocess
import tempfile
import time

from dev.dev_utils import blender_exec_path_get

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
    cmd_args = (bp,"--factory-startup") + args
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

def blender_lpy_eval_file(filepath):
    path = repr(filepath)
    py_code = f"""from basilisp_blender import eval as evl
evl.eval_file({path})
"""
    return blender_eval(py_code)
