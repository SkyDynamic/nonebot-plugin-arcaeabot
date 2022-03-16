from aiocqhttp import ActionFailed
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message
from nonebot.params import CommandArg
from nonebot.log import logger
from nonebot.exception import ActionFailed
from ..matcher import arc
from ..assets_updater import check_update


async def assets_update_handler(bot: Bot, event: MessageEvent, args: Message=CommandArg()):
    args:list = str(args).split()
    if args[0] == "assets_update":
        result = await check_update()
        try:
            await arc.finish("\n".join([f"> {event.sender.card or event.sender.nickname}",
            f"成功更新 {len(result)} 张曲绘:",
            ", ".join(result)]))
        except ActionFailed as e:
            logger.error(f'ActionFailed | {e.info["msg"].lower()} | retcode = {e.info["retcode"]} | {e.info["wording"]}')