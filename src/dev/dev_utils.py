"Development utils shared amongst scripts and tests, but excluded from the package."
import os
import platform
import shutil
import time

ENV_BLENDER_HOME_ = "BB_BLENDER_TEST_HOME"


def file_exists_wait(filepath, count_max, interval_sec):
    """Checks for the existence of `filepath` in a loop, waiting for
    `interval_sec` seconds between checks. The loop continues until
    `filepath` is found or `count_max` iteration are reached.

    """
    while count_max > 0:
        if os.path.exists(str(filepath)) and os.path.getsize(filepath) > 0:
            break
        count_max -= 1
        time.sleep(interval_sec)


def blender_home_get():
    """Returns the absolute path to the Blender home directory, as
    specified in the environment variable pointed by
    `ENV_BLENDER_HOME_`.

    `assert`s that the path exists.

    """
    blender_home = os.getenv(ENV_BLENDER_HOME_)
    assert blender_home, f":error :env-var-not-set {ENV_BLENDER_HOME_}"
    blender_home_abs = os.path.abspath(os.path.expanduser(blender_home))
    return blender_home_abs


def blender_exec_path_get():
    """Returns the path to the Blender executable in the blender home
    path obtained from `blender_home_get`, or None if the executable
    is not found.

    """
    blender_home_abs = blender_home_get()
    if platform.system() == "Darwin":
        blender_home_abs = os.path.join(blender_home_abs, "Contents/MacOS")

    exec_path = None
    envpath = os.environ.get("PATH", "")
    envpath_new = blender_home_abs
    try:
        os.environ["PATH"] = envpath_new
        exec_path = shutil.which("blender")
    finally:
        os.environ["PATH"] = envpath
    assert (
        exec_path
    ), f":error :blender-exec-not-found-in {ENV_BLENDER_HOME_}={blender_home_abs}"
    print(f":blender-found-at {ENV_BLENDER_HOME_}={blender_home_abs} :exec {exec_path}")
    return exec_path
