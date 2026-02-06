from typing import TYPE_CHECKING

import bmesh
import bpy
import mathutils


if TYPE_CHECKING:
    from ..props.asset import AssetWidget


def get_attribute(asset: "AssetWidget", name: str, default="") -> str:
    if name in asset.configurator.attributes:
        return asset.configurator.attributes[name].value
    else:
        return default


def get_property(asset: "AssetWidget", name: str, default="") -> str:
    if name in asset.configurator.properties:
        return asset.configurator.properties[name].value
    else:
        return default


def new_collection(name: str) -> bpy.types.Collection:
    child = bpy.data.collections.new(name)
    return child


def set_height_shape(obj: bpy.types.Object, value: float):
    if not obj.data.shape_keys:
        return

    for key in obj.data.shape_keys.key_blocks:
        if "height" in key.name.lower():
            key.value = value


def apply_shape_keys(obj: bpy.types.Object):
    if not obj.data.shape_keys:
        return

    key = obj.shape_key_add(from_mix=True)
    key.value = 1.0

    for key in obj.data.shape_keys.key_blocks:
        obj.shape_key_remove(key)


def apply_transforms(obj: bpy.types.Object):
    obj.location = (0.0, 0.0, 0.0)

    bm = bmesh.new()
    bm.from_mesh(obj.data)

    bm.transform(obj.matrix_basis)
    bm.normal_update()

    bm.to_mesh(obj.data)
    bm.free()

    obj.matrix_basis = mathutils.Matrix.Identity(4)
