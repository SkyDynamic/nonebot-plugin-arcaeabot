from ..matcher import arc
from ..database import UserInfo
from ..message.image_message import UserArcaeaInfo
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.params import CommandArg


async def ptt_handler(event: MessageEvent, arg: Message = CommandArg()):
    args = arg.extract_plain_text().split()
    if args[0] == "ptt":
        user_info: UserInfo = UserInfo.get_or_none(UserInfo.user_qq == event.user_id)
        if not user_info:
            await arc.finish(MessageSegment.reply(event.message_id) + "你还没绑定呢！")
        if UserArcaeaInfo.is_querying(user_info.arcaea_id):
            await arc.finish(
                MessageSegment.reply(event.message_id) + "您已在查询队列, 请勿重复发起查询。"
            )
        await arc.send(MessageSegment.reply(event.message_id) + "正在查询ptt")
        result = await UserArcaeaInfo.draw_user_ptt(user_info.arcaea_id)
        await arc.finish(MessageSegment.reply(event.message_id) + result)
