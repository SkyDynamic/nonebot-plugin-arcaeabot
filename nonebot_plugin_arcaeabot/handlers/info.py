from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, ActionFailed
from nonebot.params import CommandArg
from nonebot.log import logger
from ..matcher import arc
from ..data import UserInfo


async def info_handler(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    args: list = str(args).split()
    logger.debug(args)
    if args[0] == "info":
        user_info = UserInfo.get_or_none(
            UserInfo.user_qq == event.user_id)
        if not user_info:
            try:
                await arc.finish("\n".join([f"> {event.sender.card or event.sender.nickname}", "你还没绑定哦~"]))
            except ActionFailed as e:
                logger.exception(
                    f'ActionFailed | {e.info["msg"].lower()} | retcode = {e.info["retcode"]} | {e.info["wording"]}')
                return
        try:
            await arc.finish("\n".join([f"> {event.sender.card or event.sender.nickname}",
                                        f"id: {user_info.arcaea_id}, "
                                        f"用户名: {user_info.arcaea_name}。"]))
        except ActionFailed as e:
            logger.exception(
                f'ActionFailed | {e.info["msg"].lower()} | retcode = {e.info["retcode"]} | {e.info["wording"]}')
            return
