import bpy
from bpy.types import Context, Operator
from bpy.props import StringProperty

from .. import utils


# =========================================================
# CHỈ GIỮ OPERATOR REFRESH THƯ VIỆN LOCAL
# =========================================================

class RefreshLibraryOperator(Operator):
    bl_idname = "envirocast.refresh_library"
    bl_label = "Refresh Library"
    bl_options = {"REGISTER", "INTERNAL"}

    tooltip: StringProperty()

    @classmethod
    def description(cls, context, properties):
        return properties.tooltip

    def execute(self, context: Context):
        utils.load_library()
        self.report({"INFO"}, "Refreshed library")
        return {"FINISHED"}


# =========================================================
# REGISTER
# =========================================================

classes = (
    RefreshLibraryOperator,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)