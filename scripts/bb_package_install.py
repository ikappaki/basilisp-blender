"""Builds the package and installs in the Blender directory
returned by `dev.dev_utils.blender_home_get`, of which see.

This direct directory is typically specified by the
`BB_BLENDER_TEST_HOME` environment variable.

"""

import os
import shutil
import subprocess
import sys
import tempfile

from dev.dev_utils import blender_exec_path_get, file_exists_wait

blender_path = blender_exec_path_get()

result = subprocess.run(["poetry", "version"], capture_output=True, text=True)

bb_version = result.stdout.strip().replace("-", "_").replace(" ", "-")
wheel_path = f"dist/{bb_version}-py3-none-any.whl"
print(f"\n:installing :version {bb_version} :wheel {wheel_path} :in {blender_path}\n")
assert os.path.exists(wheel_path), f":wheel-not-found {wheel_path}"

with tempfile.TemporaryDirectory() as temp_dir:
    temp_file = os.path.join(temp_dir, "install.py")
    with open(temp_file, mode="w") as temp_file:
        temp_file.write(
            f'''import pip
pip.main(['install', {repr(wheel_path)}])
from basilisp_blender import eval as evl

evl.eval_str("""(import [pkg_resources :as pr])
(println :basilisp-blender :installed
         :version (str "basilisp_blender-" (.-version (pr/get_distribution "basilisp_blender"))))""")
'''
        )

    result = subprocess.run(
        [blender_path, "--background", "--factory-startup", "--python", temp_file.name],
        capture_output=True,
        text=True,
    )
    print(result.stderr)
    print(result.stdout)
    assert f":basilisp-blender :installed :version {bb_version}" in result.stdout
