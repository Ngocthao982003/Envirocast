import bpy
from bpy.props import StringProperty
from bpy.types import PropertyGroup, bpy_prop_collection


class BaseWidget(PropertyGroup):

    name: StringProperty(name="Name")

    @property
    def parent(self) -> "BaseWidget":
        return eval(repr(self).rpartition(".")[0])

    @property
    def parent_collection(self) -> "bpy_prop_collection":
        return eval(repr(self).rpartition("[")[0])


classes = (BaseWidget,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
