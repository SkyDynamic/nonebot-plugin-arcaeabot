from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, MessageSegment
from nonebot.params import CommandArg
from ..matcher import arc
from ..message.text_message import TextMessage


async def help_handler(event: MessageEvent, arg: Message = CommandArg()):
    args = arg.extract_plain_text().split()
    if args[0] == "help":
        await arc.finish(
            MessageSegment.reply(event.message_id) + TextMessage.help_message
        )
