from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.params import CommandArg
from ..database import UserInfo
from ..message.image_message import UserArcaeaInfo
from ..matcher import arc
from ..schema import diffstr2num
from ..config import UserUIConfig


async def info_handler(event: MessageEvent, arg: Message = CommandArg()):
    args = arg.extract_plain_text().split()
    if args[0] == "info":
        if len(args) == 1:
            user_info: UserInfo = UserInfo.get_or_none(
                UserInfo.user_qq == event.user_id
            )

            # Expection

            if not user_info:
                await arc.finish(MessageSegment.reply(event.message_id) + "你还没绑定呢！")

            if UserArcaeaInfo.is_querying(user_info.arcaea_id):
                await arc.finish(
                    MessageSegment.reply(event.message_id) + "您已在查询队列, 请勿重复发起查询。"
                )

            # Query
            await arc.send(
                MessageSegment.reply(event.message_id) + "开始查询您最近的游玩记录中，请稍后..."
            )
            user_config = UserUIConfig().read().get(str(event.user_id))
            language = user_config.get("language") if user_config else None
            ui = user_config.get("ui") if user_config else None
            result = await UserArcaeaInfo.draw_user_recent(
                arcaea_id=user_info.arcaea_id, language=language, ui=ui
            )
            await arc.finish(MessageSegment.reply(event.message_id) + result)

        if len(args) >= 2:
            user_info: UserInfo = UserInfo.get_or_none(
                UserInfo.user_qq == event.user_id
            )
            difficulty = diffstr2num(args[-1].upper())
            if difficulty is not None:
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
            await arc.send(MessageSegment.reply(event.message_id) + "开始查询Best中，请稍后...")
            user_config = UserUIConfig().read().get(str(event.user_id))
            language = user_config.get("language") if user_config else None
            ui = user_config.get("ui") if user_config else None
            result = await UserArcaeaInfo.draw_user_best(
                arcaea_id=user_info.arcaea_id,
                songname=songname,
                difficulty=difficulty,
                language=language,
                ui=ui,
            )
            await arc.finish(MessageSegment.reply(event.message_id) + result)
