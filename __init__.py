bl_info = {
    "name": "Enviroment",
    "description": "The Scattering Tools",
    "location": "View3D > Sidebar > Scatter & Geo-Nodes > Sidebar > Enviroment",
    "author": "Group26",
    "version": (7, 2, 26),
    "blender": (3, 5, 0),
    "support": "COMMUNITY",
    "category": "",
}

from . import (
    asset_manager,
    common,
    slow_task_manager,
    effects,
    environment,
    icon_viewer,
    icons,
    extras,
    scatter,
    utils,
)

modules = (
    common,
    slow_task_manager,
    icons,
    scatter,
    icon_viewer,
    asset_manager,
    effects,
    utils,
    environment,
    extras,
)


def register():
    for module in modules:
        module.register()


def unregister():
    for module in reversed(modules):
        module.unregister()
