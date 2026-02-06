from typing import TYPE_CHECKING

import bpy

from . import group26_one, group26_two, group26_three, standard

if TYPE_CHECKING:
    from ..props.asset import AssetWidget

modules = {
    "standard": standard,
    "group26_one": group26_one,
    "group26_two": group26_two,
    "group26_three": group26_three,
}


def configure(asset: "AssetWidget", lod=None, variant=None) -> bpy.types.Collection:
    module = modules.get(asset.configurator.name, standard)
    return module.configure(asset, lod, variant)
