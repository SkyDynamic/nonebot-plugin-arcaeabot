from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from nonebot.exception import ActionFailed
from nonebot.params import CommandArg
from nonebot.log import logger
from ..data import UserInfo
from ..matcher import arc

from ..adapters.utils import adapter_selector
api_in_use = adapter_selector().upper()
if api_in_use == "AUA":
    from ..adapters.aua.api import fetch_user_info
elif api_in_use == "ESTERTION":
    from ..adapters.estertion.api import fetch_user_info
else:
    logger.error("不支持的Api选项")


async def bind_handler(bot: Bot, event: MessageEvent, args=CommandArg()):
    args: list = str(args).split()
    if args[0] == "bind":
        arc_id = args[1].strip()
        if len(arc_id) != 9:
            try:
                await arc.finish("\n".join([f"> {event.sender.card or event.sender.nickname}", "id 格式错误，请检查。"]))
            except ActionFailed as e:
                logger.error(
                    f'ActionFailed | {e.info["msg"].lower()} | retcode = {e.info["retcode"]} | {e.info["wording"]}')
        if api_in_use == "AUA":
            player_name = (await fetch_user_info(arcaea_id=arc_id, recent_only=True))["content"]["account_info"]["name"]
        elif api_in_use == "ESTERTION":
            player_name = (await fetch_user_info(arcaea_id=arc_id, recent_only=True))[0]["data"]["name"]
        UserInfo.replace(user_qq=event.user_id, arcaea_id=arc_id, arcaea_name=player_name).execute()
        try:
            await arc.finish("\n".join([f"> {event.sender.card or event.sender.nickname}",
                                        f"绑定成功, 用户名: {player_name}, id: {arc_id}"]))
        except ActionFailed as e:
            logger.error(
                f'ActionFailed | {e.info["msg"].lower()} | retcode = {e.info["retcode"]} | {e.info["wording"]}')
