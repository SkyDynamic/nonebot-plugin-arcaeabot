from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.params import CommandArg
from ..database import UserInfo, ArcInfo
from ..matcher import arc


async def info_handler(event: MessageEvent, arg: Message = CommandArg()):
    args = arg.extract_plain_text().split()
    if args[0] == "info":
        user_info: UserInfo = UserInfo.get_or_none(UserInfo.user_qq == event.user_id)
        # Exception
        if not user_info:
            await arc.finish(MessageSegment.reply(event.message_id) + "你还没绑定呢！")

        arc_info: ArcInfo = ArcInfo.get_or_none(
            ArcInfo.arcaea_id == user_info.arcaea_id
        )

        await arc.finish(
            MessageSegment.reply(event.message_id)
            + f"id: {user_info.arcaea_id}, 用户名: {arc_info.arcaea_name}。"
        )
