import bpy

from .. import icons
from ..asset_manager import previews
from ..utils.getters import get_preferences
from .props import WindowManagerProps


class OpenUrlOperator(bpy.types.Operator):

    bl_idname = "envirocast.url_open"
    bl_label = "Open URL"

    url: bpy.props.StringProperty(name="URL", options={"HIDDEN", "SKIP_SAVE"})
    event: bpy.props.StringProperty(name="Event", options={"HIDDEN", "SKIP_SAVE"})
    name: bpy.props.StringProperty(name="Name", options={"HIDDEN", "SKIP_SAVE"})
    value: bpy.props.StringProperty(name="Value", options={"HIDDEN", "SKIP_SAVE"})

    tooltip: bpy.props.StringProperty(default="Open URL in Browser.")

    @classmethod
    def description(cls, context, properties):
        return properties.tooltip

    def execute(self, context: bpy.types.Context) -> set:
        bpy.ops.wm.url_open(url=self.url)
        return {"FINISHED"}

    @staticmethod
    def configure(
        op: bpy.types.OperatorProperties,
        url: str,
        event: str,
        name: str = "",
        value: str = "",
    ):
        op.url, op.event, op.name, op.value = url, event, name, value


class CloseCompatibilityWarningOperator(bpy.types.Operator):

    bl_idname = "envirocast.close_compatibility_warning"
    bl_label = "OK"

    def execute(self, context: bpy.types.Context) -> set:
        wm_props: WindowManagerProps = context.window_manager.envirocast
        wm_props.compatibility_warning = True
        prefs = get_preferences()
        if wm_props.ignore_compatibility_warning:
            prefs.ignore_compatibility_warning = True
        bpy.ops.wm.save_userpref()
        return {"FINISHED"}


classes = (
    OpenUrlOperator,
    CloseCompatibilityWarningOperator,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
