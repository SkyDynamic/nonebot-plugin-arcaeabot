from .matcher import arc
from .handler import (
    b30_handler,
    assets_update_handler,
    pre_handler,
    bind_handler,
    info_handler,
    help_handler,
    random_handler,
    song_handler,
    default_handler,
    preview_handler,
    ptt_handler,
    ui_handler
)
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="ArcaeaBot",
    description="Arcaea查分插件",
    usage="使用/arc help查看使用帮助",
    extra={
        "unique_name": "arcaeabot",
        "author": "SEAFHMC <soku_ritsuki@outlook.com>",
        "version": "3.1.3",
    },
)

arc.handle()(pre_handler)
arc.handle()(b30_handler)
arc.handle()(song_handler)
arc.handle()(preview_handler)
arc.handle()(bind_handler)
arc.handle()(info_handler)
arc.handle()(assets_update_handler)
arc.handle()(help_handler)
arc.handle()(random_handler)
arc.handle()(ptt_handler)
arc.handle()(ui_handler)
arc.handle()(default_handler)
