from ..api import API
from ..database import UserInfo, ArcInfo
from ..matcher import arc
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.params import CommandArg


async def bind_handler(event: MessageEvent, arg: Message = CommandArg()):
    args = arg.extract_plain_text().split()
    if args[0] == "bind":
        if len(args) == 1:
            await arc.finish(MessageSegment.reply(event.message_id) + "缺少参数 arcaea_id！")

        arc_id = args[1]

        arc_info: ArcInfo = ArcInfo.get_or_none(
            (ArcInfo.arcaea_name == arc_id) | (ArcInfo.arcaea_id == arc_id)
        )
        if arc_info:
            arc_id = arc_info.arcaea_id
            arc_name = arc_info.arcaea_name

        # Not finished yet
        return
