bl_info = {
    "name"    : "Basilisp nREPL Server Control Panel",
    "description" : "Control the nREPL server from the Properties Editor>Output panel",
    "author"  : "ikappaki",
    "version" : (0, 99, 99),
    "blender" : (3, 60, 0),
    "location": "Properties Editor>Output",
    "doc_url" : "https://github.com/ikappaki/basilisp-blender",
    "category": "Development",
}

# >>>###<<< Marker: Start Of Code
from basilisp_blender import control_panel_create
_DESTROY_FN = None
def register():
    global _DESTROY_FN
    print(f"nREPL Control Panel creating...")
    _DESTROY_FN = control_panel_create()
    print(f"nREPL Control Panel creating... done")

def unregister():
    global _DESTROY_FN
    print("nREPL Control Panel destroying...")
    _DESTROY_FN()
    _DESTROY_FN = None
    print("nREPL Control Panel destroying... done")
