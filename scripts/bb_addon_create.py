# This script should be invoked from the project root directory.
#
# Copies the nrepl_panel_addon.py file to out/ adding the version
# number as retrieved from `poetry version`.
import os
import re
import subprocess

src_path = "src/dev/nrepl_panel_addon.py"
version_mark = "(0, 99, 99)"

result = subprocess.run(["poetry", "version"], capture_output=True, text=True)
_, version = result.stdout.split(" ")
major, minor, patch = version.split(".")
patch_int = int(re.match(r"^\d+", patch).group())

os.makedirs("out", exist_ok=True)
out_path = f'out/nrepl_panel_addon_{version.strip().replace(".", "_")}.py'

with open(src_path, "r") as src:
    with open(out_path, "w", newline="\n") as dst:
        dst.write(f"# Autogenerated from {src_path}\n")
        for line in src.readlines():
            if version_mark in line:
                line = line.replace(version_mark, f"({major}, {minor}, {patch_int})")
            dst.write(line)
print(f":bb_addon_create.py :created {out_path}")
