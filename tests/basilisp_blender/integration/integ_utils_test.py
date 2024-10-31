import os
from dev.dev_utils import blender_exec_path_get, file_exists_wait
from tests.basilisp_blender.integration.integ_utils import blender_eval, blender_eval_file, blender_lpy_eval, blender_run

import pytest

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
        assert ":running..." in out
    finally:
        process.terminate()


def test_blender_lpy_eval():
    result = blender_lpy_eval("(+ 1024 1024)")
    assert ":lpy-result 2048" in result.stdout

