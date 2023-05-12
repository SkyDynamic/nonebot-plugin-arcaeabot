from ..matcher import arc
from ..database import UserInfo
from ..config import UserUIConfig
from ..message.image_message import UserArcaeaInfo
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.params import CommandArg


async def b30_handler(event: MessageEvent, arg: Message = CommandArg()):
    args = arg.extract_plain_text().split()
    if args[0] == "b30" or args[0] == "b40":
        if len(args) == 1:
            user_info: UserInfo = UserInfo.get_or_none(
                UserInfo.user_qq == event.user_id
            )
            if not user_info:
                await arc.finish(MessageSegment.reply(event.message_id) + "你还没绑定呢！")
            if UserArcaeaInfo.is_querying(user_info.arcaea_id):
                await arc.finish(
                    MessageSegment.reply(event.message_id) + "您已在查询队列, 请勿重复发起查询。"
                )
            await arc.send(
                MessageSegment.reply(event.message_id) + "开始查询Bests30中，请稍后..."
            )
            user_config = UserUIConfig().read().get(str(event.user_id))
            language = user_config.get("language") if user_config else None
            result = await UserArcaeaInfo.draw_user_b30(language, user_info.arcaea_id)
            await arc.finish(MessageSegment.reply(event.message_id) + result)
        elif len(args) == 2:
            querying = list()
            if event.user_id in querying:
                await arc.finish(
                    MessageSegment.reply(event.message_id) + "您已在查询队列, 请勿重复发起查询。"
                )
            querying.append(event.user_id)
            await arc.send(
                MessageSegment.reply(event.message_id) + "开始查询Bests30中，请稍后..."
            )
            result = await UserArcaeaInfo.draw_user_b30(
                language="en", arcaea_id=args[1]
            )
            querying.remove(event.user_id)
            await arc.finish(MessageSegment.reply(event.message_id) + result)
