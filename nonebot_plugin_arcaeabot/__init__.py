from .matcher import arc, ai_cmd
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
    Ai_query_reset_scheduler,
    calc_handler,
)

import nonebot
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="ArcaeaBot",
    description="Arcaea查分插件",
    usage="使用/arc help查看使用帮助",
    extra={
        "unique_name": "arcaeabot",
        "author": [
            "SEAFHMC <soku_ritsuki@outlook.com>" "SkyDynamic <SkyDynamic@outlook.com>"
        ],
        "version": "3.1.20",
    },
)

# Cheak Update
from apscheduler.schedulers.background import BackgroundScheduler
Check_Update_scheduler = BackgroundScheduler()
@Check_Update_scheduler.scheduled_job("cron", hour="22")
async def Check_Update():
    from httpx import AsyncClient
    client = AsyncClient()
    try:
        result: dict = await client.get("https://raw.kgithub.com/SEAFHMC/nonebot-plugin-arcaeabot/v3.0.0/version.json").json()
        new_version = str(result.get('version')).split(".")
        current_version = str(__plugin_meta__.extra.get('version')).split(".")
        if new_version[0] > current_version[0] or new_version[1] > current_version[1] or new_version[2] > current_version[2]:
            await safe_send('.'.join(current_version), '.'.join(new_version))
    except:
        pass

async def safe_send(current_version, new_version):
    try:
        # 获取已连接的Bot
        bots = nonebot.get_bots()
        # 遍历字典里的Bot类
        for bot in bots.values():
            # 获取所有群
            group_id_list = list()
            group_info_list = await bot.call_api('get_group_list')

            # 将所有群号加入列表
            for group_info in group_info_list:
                group_id_list.append(group_info['group_id'])

            for group_id in group_id_list:
                # 发送信息
                bot.call_api(
                api='send_group_msg',
                **{
                    'group_id': group_id,
                    'message': f'Nonebot_Plugin_ArcaeaBot有新版本！\n当前版本: {current_version}\n最新版本: {new_version}'
                }
                )
        return True
    except Exception as e:
        return False

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
arc.handle()(calc_handler)
arc.handle()(ui_handler)
ai_cmd.handle()(ai_handler)
ai_cmd.got("code")(ai_first_handler)
ai_cmd.got("code_")(ai_continue_handler)
arc.handle()(default_handler)
