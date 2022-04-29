from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, MessageSegment
from nonebot.params import CommandArg
from ..matcher import arc
from ..draw_text import draw_help


async def help_handler(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    args: list = str(args).split()
    if args[0] == "help":
        await arc.finish(MessageSegment.reply(event.message_id) + draw_help())
