from typing import TYPE_CHECKING

import bpy
from bpy.types import Context, Panel
from bpy_extras import asset_utils

from . import default
from .asset_browser import get_asset_browser_windows

if TYPE_CHECKING:
    from .props.library import LibraryWidget


class EnviroCastAssetBrowserPanel(asset_utils.AssetMetaDataPanel, Panel):
    bl_idname = "ENVIROCAST_PT_AssetBrowserPanel"
    bl_label = "Envirocast"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context: Context):
        return (
            get_asset_browser_windows()
            and context.window in get_asset_browser_windows()
        )

    def draw(self, context: Context):
        layout = self.layout
        active_file = context.active_file
        library: "LibraryWidget" = context.window_manager.envirocast.library
        params = context.area.spaces.active.params

        if active_file:
            library.draw_products(context, layout)

        # CHỈ giữ logic hiển thị – bỏ hoàn toàn delete catalog
        if (
            params.catalog_id == default.ASSETS_CATALOG_ID
            or params.catalog_id == default.ENVIRONMENTS_CATALOG_ID
        ):
            return


def disable_metadata_panel(cls, context: Context):
    if (
        not get_asset_browser_windows()
        or context.window not in get_asset_browser_windows()
    ) or (
        not hasattr(context.area.spaces.active.params, "asset_library_reference")
        and not hasattr(context.area.spaces.active.params, "asset_library_ref")
    ):
        return cls.poll_orig(context)
    return False


def draw_envirocast_browser_header(self, context: Context):
    # CHỈ GIỮ HEADER CƠ BẢN – KHÔNG CÒN INSTALL/SYNC

    if (
        not get_asset_browser_windows()
        or context.window not in get_asset_browser_windows()
    ):
        self.draw_orig(context)
        return

    if not hasattr(
        context.area.spaces.active.params, "asset_library_ref"
    ) and not hasattr(context.area.spaces.active.params, "asset_library_reference"):
        self.draw_orig(context)
        return

    params = context.space_data.params
    layout: bpy.types.UILayout = self.layout

    layout.box().label(text="EnviroCast Asset Browser", icon="ASSET_MANAGER")
    layout.separator_spacer()

    # Chỉ giữ search
    sub = layout.row()
    sub.ui_units_x = 8
    sub.prop(params, "filter_search", text="", icon="VIEWZOOM")

    layout.separator_spacer()

    # Chỉ giữ display type
    layout.prop_with_popover(
        params,
        "display_type",
        panel="ASSETBROWSER_PT_display",
        text="",
        icon_only=True,
    )


classes = (EnviroCastAssetBrowserPanel,)


def update_poll(type):
    type.poll_orig = type.poll
    type.poll = classmethod(disable_metadata_panel)


def revert_poll(type):
    type.poll = type.poll_orig


def register():
    update_poll(bpy.types.ASSETBROWSER_PT_metadata)
    update_poll(bpy.types.ASSETBROWSER_MT_editor_menus)
    update_poll(bpy.types.ASSETBROWSER_PT_metadata_preview)
    update_poll(bpy.types.ASSETBROWSER_PT_metadata_tags)

    bpy.types.FILEBROWSER_HT_header.draw_orig = bpy.types.FILEBROWSER_HT_header.draw
    bpy.types.FILEBROWSER_HT_header.draw = draw_envirocast_browser_header

    asset_utils.AssetBrowserPanel.poll_orig = asset_utils.AssetBrowserPanel.poll
    asset_utils.AssetBrowserPanel.poll = classmethod(disable_metadata_panel)

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    revert_poll(bpy.types.ASSETBROWSER_PT_metadata)
    revert_poll(bpy.types.ASSETBROWSER_MT_editor_menus)
    revert_poll(bpy.types.ASSETBROWSER_PT_metadata_preview)
    revert_poll(bpy.types.ASSETBROWSER_PT_metadata_tags)

    bpy.types.FILEBROWSER_HT_header.draw = bpy.types.FILEBROWSER_HT_header.draw_orig
    asset_utils.AssetBrowserPanel.poll = asset_utils.AssetBrowserPanel.poll_orig

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
