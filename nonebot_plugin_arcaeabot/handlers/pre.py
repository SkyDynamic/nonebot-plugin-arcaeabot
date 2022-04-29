from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, MessageSegment
from nonebot.params import CommandArg
from ..matcher import arc
from ..config import config
from ..draw_text import draw_help


async def pre_handler(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    args: list = str(args).split()
    if len(args) == 0:
        await arc.finish(MessageSegment.reply(event.message_id) + draw_help())

    elif args[0] not in [
        "help",
        "info",
        "recent",
        "b30",
        "bind",
        "unbind",
        "assets_update",
        "best",
        "b40",
        "random",
        "song",
        "songs",
    ]:
        await arc.finish("不支持的命令参数")
    aua_ua = config.get_config("aua_ua")
    aua_url = config.get_config("aua_url")
    if aua_ua == 'SECRET' or aua_url == 'URL':
        await arc.finish("ArcaeaUnlimitedApi is not configured!")
