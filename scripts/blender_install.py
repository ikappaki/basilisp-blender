"""Downloads the specified version of Blender (passed as the first
argument) to the output directory returned
by`dev.dev_utils.blender_home_get`, of which see.

The directory is typically specified by the `BB_BLENDER_TEST_HOME`
environment variable.

"""

import os
import platform
import shutil
import sys

import requests

from dev.dev_utils import blender_home_get

tmp_dir = ".bb-tmp"

version = None
outpath = None
assert len(sys.argv) == 2, "usage: blender_install.py <blender-version-as-x.y.z>"

(version,) = tuple(sys.argv)[1:]
print(f":args :version {version}")
assert version.count(".") == 2, f":error :expected-two-dots-in-version {version}"

version_short = version[: version.rfind(".")]

outdir = blender_home_get()
print(f":destination {outdir}")

system = platform.system()

filename = None
extension = None
if system == "Windows":
    filename = f"blender-{version}-windows-x64.zip"
    extension = ".zip"
elif system == "Linux":
    filename = f"blender-{version}-linux-x64.tar.xz"
    extension = ".tar.xz"
elif system == "Darwin":
    filename = f"blender-{version}-macos-arm64.dmg"
    extension = ".dmg"

assert filename, f":error :system-unsupported {system}"
assert extension

filename_path = os.path.join(tmp_dir, filename)
url = f"https://download.blender.org/release/Blender{version_short}/{filename}"
outdir_abs = os.path.abspath(os.path.expanduser(outdir))
assert not os.path.exists(outdir_abs), f":error :outdir {outdir_abs} :exists-already"

os.makedirs(tmp_dir, exist_ok=True)

print(f"\n:downloading {url} :to {filename_path}")

with requests.get(url, stream=True) as response:
    response.raise_for_status()
    with open(filename_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=1024 * 1024 * 10):
            print("*", end="", flush=True)
            file.write(chunk)

print(f"\n:download :done")
assert os.path.exists(filename_path)

if system == "Darwin":
    extract_base = "/Volumes"
    extract_dir = "/Volumes/Blender/Blender.app"
else:
    extract_base = tmp_dir
    extract_dir = os.path.join(tmp_dir, filename[: filename.rfind(extension)])

print(f"\n:extracting {filename_path} :to {extract_base} :as {extract_dir}")
if system == "Windows":
    import zipfile

    with zipfile.ZipFile(filename_path) as zip_ref:
        zip_ref.extractall(extract_base)
elif system == "Linux":
    import tarfile

    with tarfile.open(filename_path) as tar:
        tar.extractall(path=extract_base)
elif system == "Darwin":
    import subprocess

    result = subprocess.run(
        ["hdiutil", "attach", filename_path], check=True, capture_output=True, text=True
    )
    print(f":process :stdout {result.stdout}")
    print(f":process :stderr {result.stderr}")
    extract_dir = "/Volumes/Blender/Blender.app"
print(f":extract :done")
assert os.path.exists(extract_dir)

if system == "Darwin":
    print(f"\n:copying {extract_dir} :to {outdir_abs}")
    shutil.copytree(extract_dir, outdir_abs)
    print(f":copying :done")
else:
    print(f"\n:moving {extract_dir} :to {outdir_abs}")
    shutil.move(extract_dir, outdir_abs)
    print(f":move :done")
assert outdir_abs
