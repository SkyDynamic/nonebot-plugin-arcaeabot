from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, MessageSegment
from nonebot.params import CommandArg
from ..matcher import arc
from ..data import UserInfo
from ..draw_image import UserArcaeaInfo


async def recent_handler(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    args: list = str(args).split()
    if args[0] == "recent":
        user_info = UserInfo.get_or_none(UserInfo.user_qq == event.user_id)

        # Expection
        if len(args) != 1:
            await arc.finish(MessageSegment.reply(event.message_id) + "不支持的命令参数")

        if not user_info:
            await arc.finish(MessageSegment.reply(event.message_id) + "你还没绑定呢！")

        if UserArcaeaInfo.is_querying(user_info.arcaea_id):
            await arc.finish(MessageSegment.reply(event.message_id) + "您已在查询队列, 请勿重复发起查询。")

        # Query
        result = await UserArcaeaInfo.draw_recent_image(arcaea_id=user_info.arcaea_id)
        await arc.finish(MessageSegment.reply(event.message_id) + result)

