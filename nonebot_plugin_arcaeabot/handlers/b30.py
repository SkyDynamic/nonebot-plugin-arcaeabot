from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
    Message,
    ActionFailed,
    MessageSegment,
)
from nonebot.params import CommandArg
from nonebot.log import logger
from ..matcher import arc
from ..data import UserInfo
from ..draw_image import UserArcaeaInfo


async def b30_handler(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    args: list = str(args).split()
    if args[0] == "b30" or args[0] == "b40":
        # check
        user_info = UserInfo.get_or_none(UserInfo.user_qq == event.user_id)
        if not user_info:
            await arc.finish(
                "\n".join(
                    [f"> {event.sender.card or event.sender.nickname}", "你还没绑定哦~"]
                )
            )

        #query
        if not UserArcaeaInfo.is_querying(user_info.arcaea_id):
            result = await UserArcaeaInfo.draw_best30_image(user_info.arcaea_id)
            await arc.finish(MessageSegment.reply(event.message_id) + result)

        #expection
        else:
            await arc.finish(
                "\n".join(
                    [
                        f"> {event.sender.card or event.sender.nickname}",
                        "您已在查询队列, 请勿重复发起查询。",
                    ]
                )
            )
            