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

        resp = await API.get_user_info(arcaea_id=arc_id)
        if error_message := resp.message:
            await arc.finish(MessageSegment.reply(event.user_id) + error_message)
        arc_id = resp.content.account_info.code
        arc_name = resp.content.account_info.name
        ArcInfo.replace(
            arcaea_id=arc_id,
            arcaea_name=arc_name,
            ptt=resp.content.account_info.rating,
        ).execute()
        UserInfo.delete().where(UserInfo.user_qq == event.user_id).execute()
        UserInfo.replace(user_qq=event.user_id, arcaea_id=arc_id).execute()
        await arc.finish(
            MessageSegment.reply(event.message_id)
            + f"绑定成功, 用户名: {arc_name}, id: {arc_id}"
        )
