from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
from ..matcher import arc


async def default_handler(event: MessageEvent):
    await arc.finish(MessageSegment.reply(event.message_id) + "不支持的命令参数")
