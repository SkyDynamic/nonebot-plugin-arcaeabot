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
    ui_handler,
    ai_handler,
    ai_first_handler,
    ai_continue_handler,
    Ai_query_reset_scheduler
    )
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="ArcaeaBot",
    description="Arcaea查分插件",
    usage="使用/arc help查看使用帮助",
    extra={
        "unique_name": "arcaeabot",
        "author": [
            "SEAFHMC <soku_ritsuki@outlook.com>"
            "SkyDynamic <SkyDynamic@outlook.com>"],
        "version": "3.1.10",
    },
)

Ai_query_reset_scheduler.start()

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
arc.handle()(ai_handler)
arc.got('code', '1: 推荐一首歌给我吧\n2: 结束会话(不需要请务必回复此代码否侧返回未知参数)\n(输入数字代码，不要输入其他的)')(ai_first_handler)
arc.got('code_', '1: 再推荐一首歌给我吧!\n2: 好耶, 冲冲冲!\n3: 结束会话(不需要请务必回复此代码否侧返回未知参数)\n(输入数字代码，不要输入其他的)')(ai_continue_handler)
arc.handle()(default_handler)
