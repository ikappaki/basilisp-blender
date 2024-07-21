import pytest

from tests.basilisp_blender.integration import test_utils as tu

pytestmark = pytest.mark.integration


def test_eval_editor():
    result = tu.blender_eval(
        """from basilisp_blender import eval as evl
import bpy
before = 0
for obj in bpy.data.objects:
  if obj.name.startswith("Suzanne"):
    before += 1

block = bpy.data.texts.new(name="basilisp-blender-test")
block.write("(import bpy) (-> bpy/ops .-mesh (.primitive_monkey_add ** :location [0,0,0]))")
evl.eval_editor("basilisp-blender-test")

after = 0
for obj in bpy.data.objects:
  if obj.name.startswith("Suzanne"):
    after += 1
print(f":result :before {before} :after {after}")
"""
    )
    assert ":result :before 0 :after 1" in result.stdout
