from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.params import CommandArg
from ..database import UserInfo
from ..message.image_message import UserArcaeaInfo
from ..matcher import arc
from ..schema import diffstr2num


async def best_handler(event: MessageEvent, arg: Message = CommandArg()):
    """
    /arc best Fracture Ray ftr
    """
    args = arg.extract_plain_text().split()
    if len(args) >= 2 and args[0] == "best":
        user_info: UserInfo = UserInfo.get_or_none(UserInfo.user_qq == event.user_id)
        # get args
        if difficulty := diffstr2num(args[-1].upper()):
            songname = " ".join(args[1:-1])
        else:
            difficulty = 2
            songname = " ".join(args[1:])
        # Exception
        if not user_info:
            await arc.finish(MessageSegment.reply(event.message_id) + "你还没绑定呢！")

        if UserArcaeaInfo.is_querying(user_info.arcaea_id):
            await arc.finish(
                MessageSegment.reply(event.message_id) + "您已在查询队列, 请勿重复发起查询。"
            )
        # Query
        result = await UserArcaeaInfo.draw_user_best(
            arcaea_id=user_info.arcaea_id, songname=songname, difficulty=difficulty
        )
        await arc.finish(MessageSegment.reply(event.message_id) + result)
