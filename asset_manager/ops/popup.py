from typing import TYPE_CHECKING

import bpy

from ...utils.getters import get_preferences

from ...utils import wrap_text
from .. import utils

if TYPE_CHECKING:
    from ...common.props import WindowManagerProps
    from ..props.library import LibraryWidget

_popup_active = False


class OpenPreviewPopup(bpy.types.Operator):
    bl_idname = "envirocast.bigger_preview_asset_browser"
    bl_label = "Open Asset Preview"
    bl_description = "Show the full-size preview in a popup"

    icon_id: bpy.props.StringProperty()

    def draw(self, context):
        layout = self.layout
        icon_id = eval(self.icon_id)
        ui_scale = ui_scale = bpy.context.preferences.system.ui_scale
        layout.template_icon(
            icon_value=icon_id,
            scale=utils.icon_scale_from_res(
                int((context.region.height / 1.2) / ui_scale)
            ),
        )

    def invoke(self, context, event):
        ui_scale = ui_scale = bpy.context.preferences.system.ui_scale
        return context.window_manager.invoke_popup(
            self, width=int((context.region.height / 1.2) / ui_scale)
        )

    def execute(self, context):
        return {"FINISHED"}


class ReadDescriptionPopup(bpy.types.Operator):
    bl_idname = "envirocast.read_deascription"
    bl_label = "Description"
    bl_description = "Popup to read full description"

    bl_options = {"REGISTER"}

    name: bpy.props.StringProperty()
    description: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=450)

    def execute(self, context):
        return {"FINISHED"}

    def draw_header(self, context):
        self.layout.label(self.name)

    def draw(self, context):
        layout = self.layout
        system = bpy.context.preferences.system
        for text in wrap_text(
            self.description, width=450 * system.ui_scale
        ):
            row = layout.row()
            row.scale_y = 0.6
            row.label(text=text)
        layout.separator()


class MessagePopup(bpy.types.Operator):
    bl_idname = "envirocast.popup_message"
    bl_label = "Message"
    bl_description = "Draw the given message in a popup"
    bl_options = {"REGISTER", "INTERNAL"}

    message: bpy.props.StringProperty(name="Message")
    width: bpy.props.IntProperty(name="Width")

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event) -> set:
        return context.window_manager.invoke_props_dialog(self, width=self.width)

    def execute(self, context: bpy.types.Context) -> set:
        return {"FINISHED"}

    def draw(self, context: bpy.types.Context):
        layout = self.layout
        box = layout.box()

        column = box.column(align=True)
        column.scale_y = 0.8

        for line in self.message.splitlines():
            column.label(text=line)


class FilterPopup(bpy.types.Operator):
    bl_idname = "envirocast.popup_filter"
    bl_label = "Filter Popup"
    bl_description = "Popup to select the different filters"
    bl_options = {"REGISTER"}

    def check(self, context: bpy.types.Context) -> bool:
        return True

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event) -> set:
        return utils.draw_popup(self, context, event, width=200)

    def draw(self, context: bpy.types.Context):
        G: "WindowManagerProps" = context.window_manager.envirocast
        library: "LibraryWidget" = G.library
        library.draw_tags(self.layout)

    def execute(self, context: bpy.types.Context) -> set:
        return {"FINISHED"}


class AssetBrowserPopup(bpy.types.Operator):
    bl_idname = "envirocast.popup_browser"
    bl_label = "Asset Browser"
    bl_description = "Access library.\n\u2022 SHIFT click to reload library."
    bl_options = {"REGISTER"}

    CARD_WIDTH = 200

    use_mini_browser: bpy.props.BoolProperty(default=False)
    effect_name: bpy.props.StringProperty()
    input_name: bpy.props.StringProperty()

    def check(self, context: bpy.types.Context) -> bool:
        return True

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event) -> set:
        global _popup_active

        if not _popup_active:
            _popup_active = True
        else:
            return {"CANCELLED"}

        if event.shift:
            utils.load_library()

        prefs = get_preferences()
        panel_size = prefs.asset_browser_columns * self.CARD_WIDTH
        details_size = (self.CARD_WIDTH * 2) - 2
        self.split_factor = utils.calc_split_factor(panel_size, details_size)

        return utils.draw_popup(self, context, event, panel_size, True, True)

    def execute(self, context: bpy.types.Context) -> set:
        global _popup_active
        _popup_active = False
        return {"FINISHED"}

    def cancel(self, context: bpy.types.Context):
        global _popup_active
        _popup_active = False

    def draw(self, context: bpy.types.Context):
        library: "LibraryWidget" = context.window_manager.envirocast.library
        if self.use_mini_browser:
            library.draw_item_selector(self.layout, self.effect_name, self.input_name)
        else:
            library.draw(self.layout, self.split_factor)


class Group26AssetLibraryPopup(bpy.types.Operator):
    bl_idname = "envirocast.group26_asset_library"
    bl_label = "Asset Browser"
    bl_description = "\n\u2022".join(
        (
            "Access library.",
            "Shift click to reload library.",
        )
    )
    bl_options = {"REGISTER"}

    def execute(self, context):
        return {"FINISHED"}


classes = (
    OpenPreviewPopup,
    ReadDescriptionPopup,
    MessagePopup,
    FilterPopup,
    AssetBrowserPopup,
    Group26AssetLibraryPopup,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
