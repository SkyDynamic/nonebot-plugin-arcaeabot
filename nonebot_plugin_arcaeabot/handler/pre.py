from ..matcher import arc
from ..config import config
from ..message import TextMessage
from nonebot.log import logger
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.params import CommandArg


async def pre_handler(event: MessageEvent, arg: Message = CommandArg()):
    args = arg.extract_plain_text().split()
    if len(args) == 0:
        await arc.finish(
            MessageSegment.reply(event.message_id) + TextMessage.help_message
        )

    aua_ua = config.get_config("aua_ua")
    aua_url = config.get_config("aua_url")
    if aua_ua == "SECRET" or aua_url == "URL":
        logger.error("ArcaeaUnlimitedApi is not configured!")
        await arc.finish("ArcaeaUnlimitedApi is not configured!")
