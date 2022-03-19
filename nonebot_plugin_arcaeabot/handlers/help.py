from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, ActionFailed
from nonebot.params import CommandArg
from nonebot.log import logger
from ..matcher import arc


async def help_handler(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    args: list = str(args).split()
    logger.debug(args)
    if args[0] == "help":
        try:
            await arc.finish("\n".join(["/arc bind {arcaea id} 进行绑定。",
                                        "/arc unbind 解除绑定。",
                                        "/arc info 查看绑定信息。",
                                        "/arc recent 查询上一次游玩记录。",
                                        "/arc b30 查询 best 30 记录。"]))
        except ActionFailed as e:
            logger.error(
                    f'ActionFailed | {e.info["msg"].lower()} | retcode = {e.info["retcode"]} | {e.info["wording"]}')
