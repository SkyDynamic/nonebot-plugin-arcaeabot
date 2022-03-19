from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message
from nonebot.params import CommandArg
from ..matcher import arc


async def pre_handler(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    args: list = str(args).split()
    if args[0] not in ["help", "info", "recent", "b30", "bind", "unbind", "assets_update"]:
        await arc.finish("不支持的命令参数")
