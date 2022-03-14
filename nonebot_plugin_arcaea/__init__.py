"""
 - Author: DiheChen
 - Date: 2021-08-15 22:00:47
 - LastEditTime: 2021-08-22 02:35:04
 - LastEditors: DiheChen
 - Description: None
 - GitHub: https://github.com/Chendihe4975
"""
from loguru import logger
from nonebot.plugin import on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11 import Event, MessageEvent
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.exception import ActionFailed, FinishedException
from nonebot.params import State
from .data import UserInfo
from .draw_image import UserArcaeaInfo
from .assets_updater import check_update
from .request import fetch_user_info

matcher = on_command("/arc", aliases={"arcaea", "/a"}, priority=1, block=True)


@matcher.handle()
async def _(bot: Bot, event: Event, state: T_State=State()):
    if isinstance(event, MessageEvent):
        if (msg := event.get_plaintext().split()):
            if msg[0] not in ["help", "info", "recent", "b30", "bind", "unbind", "assets_update"]:
                try:
                    await matcher.finish("不支持的命令。")
                except ActionFailed as e:
                    logger.exception(
                        f'ActionFailed | {e.info["msg"].lower()} | retcode = {e.info["retcode"]} | {e.info["wording"]}')
                    raise FinishedException
            state["cmd"] = msg[0]
            try:
                if msg[1].isdigit() and len(msg[1]) == 9:
                    state["option"] = msg[1]
            except IndexError:
                pass
    else:
        logger.warning("Not supported: Arcaea.")
        return


@matcher.got("cmd", prompt="请补全参数。")
async def _(bot: Bot, event: Event):
    if isinstance(event, MessageEvent):
        if (msg := event.get_plaintext()):

            if msg == "help":
                try:
                    await matcher.finish("\n".join(["/a bind {arcaea id} 进行绑定。",
                                                    "/a unbind 解除绑定。",
                                                    "/a info 查看绑定信息。",
                                                    "/a recent 查询上一次游玩记录。",
                                                    "/a b30 查询 best 30 记录。"]))
                except ActionFailed as e:
                    logger.exception(
                        f'ActionFailed | {e.info["msg"].lower()} | retcode = {e.info["retcode"]} | {e.info["wording"]}')
                    return

            if msg.startswith("bind"):
                arc_id = int(msg.split()[-1])
                if len(str(arc_id)) != 9:
                    try:
                        await matcher.finish("\n".join([f"> {event.sender.card or event.sender.nickname}", "id 格式错误，请检查。"]))
                    except ActionFailed as e:
                        logger.exception(
                            f'ActionFailed | {e.info["msg"].lower()} | retcode = {e.info["retcode"]} | {e.info["wording"]}')
                        return
                player_name = (await fetch_user_info(arcaea_id=int(arc_id), recent_only=True))[0]["data"]["name"]
                UserInfo.replace(user_qq=event.user_id,
                                 arcaea_id=arc_id, arcaea_name=player_name).execute()
                try:
                    await matcher.finish(
                        "\n".join([f"> {event.sender.card or event.sender.nickname}",
                                  f"绑定成功, 用户名: {player_name}, id: {arc_id}"])
                    )
                except ActionFailed as e:
                    logger.exception(
                        f'ActionFailed | {e.info["msg"].lower()} | retcode = {e.info["retcode"]} | {e.info["wording"]}')
                    return

            if msg == "unbind":
                result = UserInfo.delete().where(
                    UserInfo.user_qq == event.user_id
                ).execute()
                try:
                    await matcher.finish("\n".join([f"> {event.sender.card or event.sender.nickname}",
                                                    "已成功删除用户记录。"]))
                except ActionFailed as e:
                    logger.exception(
                        f'ActionFailed | {e.info["msg"].lower()} | retcode = {e.info["retcode"]} | {e.info["wording"]}')
                    return

            if msg == "info":
                user_info = UserInfo.get_or_none(
                    UserInfo.user_qq == event.user_id)
                if not user_info:
                    try:
                        await matcher.finish("\n".join([f"> {event.sender.card or event.sender.nickname}", "你还没绑定哦~"]))
                    except ActionFailed as e:
                        logger.exception(
                            f'ActionFailed | {e.info["msg"].lower()} | retcode = {e.info["retcode"]} | {e.info["wording"]}')
                        return
                try:
                    await matcher.finish(
                        "\n".join([f"> {event.sender.card or event.sender.nickname}",
                                   f"id: {result.arcaea_id}, "
                                   f"用户名: {result.arcaea_name}。"])
                    )
                except ActionFailed as e:
                    logger.exception(
                        f'ActionFailed | {e.info["msg"].lower()} | retcode = {e.info["retcode"]} | {e.info["wording"]}')
                    return

            if msg == "recent":
                user_info = UserInfo.get_or_none(
                    UserInfo.user_qq == event.user_id)
                if not user_info:
                    try:
                        await matcher.finish("\n".join([f"> {event.sender.card or event.sender.nickname}", "你还没绑定哦~"]))
                    except ActionFailed as e:
                        logger.exception(
                            f'ActionFailed | {e.info["msg"].lower()} | retcode = {e.info["retcode"]} | {e.info["wording"]}')
                        return
                if not UserArcaeaInfo.is_querying(arcaea_id=int(user_info.arcaea_id)):
                    result = await UserArcaeaInfo.draw_recent_image(
                        arcaea_id=int(user_info.arcaea_id))
                    try:
                        await matcher.finish(MessageSegment.reply(event.message_id) + result)
                    except ActionFailed as e:
                        logger.exception(
                            f'ActionFailed | {e.info["msg"].lower()} | retcode = {e.info["retcode"]} | {e.info["wording"]}')
                        return
                else:
                    try:
                        await matcher.finish("\n".join([f"> {event.sender.card or event.sender.nickname}",
                                                        "您已在查询队列, 请勿重复发起查询。"]))
                    except ActionFailed as e:
                        logger.exception(
                            f'ActionFailed | {e.info["msg"].lower()} | retcode = {e.info["retcode"]} | {e.info["wording"]}')
                        return

            if msg == "b30":
                user_info = UserInfo.get_or_none(
                    UserInfo.user_qq == event.user_id)
                if not user_info:
                    try:
                        await matcher.finish("\n".join([f"> {event.sender.card or event.sender.nickname}", "你还没绑定哦~"]))
                    except ActionFailed as e:
                        logger.exception(
                            f'ActionFailed | {e.info["msg"].lower()} | retcode = {e.info["retcode"]} | {e.info["wording"]}')
                        return
                if not UserArcaeaInfo.is_querying(user_info.arcaea_id):
                    result = await UserArcaeaInfo.draw_best30_image(user_info.arcaea_id)
                    try:
                        await matcher.finish(MessageSegment.reply(event.message_id) + result)
                    except ActionFailed as e:
                        logger.exception(
                            f'ActionFailed | {e.info["msg"].lower()} | retcode = {e.info["retcode"]} | {e.info["wording"]}')
                        return
                else:
                    try:
                        await matcher.finish("\n".join([f"> {event.sender.card or event.sender.nickname}",
                                                        "您已在查询队列, 请勿重复发起查询。"]))
                    except ActionFailed as e:
                        logger.exception(
                            f'ActionFailed | {e.info["msg"].lower()} | retcode = {e.info["retcode"]} | {e.info["wording"]}')
                        return

            if msg == "assets_update":
                result = await check_update()
                try:
                    await matcher.finish("\n".join([f"> {event.sender.card or event.sender.nickname}",
                                                    f"成功更新 {len(result)} 张曲绘:",
                                                    ", ".join(result)]))
                except ActionFailed as e:
                    logger.exception(
                        f'ActionFailed | {e.info["msg"].lower()} | retcode = {e.info["retcode"]} | {e.info["wording"]}')
                    return
    else:
        logger.warning("Not supported: Arcaea.")
        return
