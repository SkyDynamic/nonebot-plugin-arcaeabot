from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, ActionFailed
from nonebot.params import CommandArg
from nonebot.log import logger
from ..matcher import arc
from ..data import UserInfo


async def unbind_handler(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    args: list = str(args).split()
    logger.debug(args)
    if args[0] == "unbind":
        result = UserInfo.delete().where(
            UserInfo.user_qq == event.user_id
        ).execute()
        try:
            await arc.finish("\n".join([f"> {event.sender.card or event.sender.nickname}",
                                        "已成功删除用户记录。"]))
        except ActionFailed as e:
            logger.exception(
                f'ActionFailed | {e.info["msg"].lower()} | retcode = {e.info["retcode"]} | {e.info["wording"]}')
