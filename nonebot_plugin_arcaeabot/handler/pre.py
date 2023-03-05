from ..matcher import arc
from ..config import config
from ..database import UserInfo
from ..config import UserUIConfig
from ..message.image_message import UserArcaeaInfo
from nonebot.log import logger
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.params import CommandArg


async def pre_handler(event: MessageEvent, arg: Message = CommandArg()):
    args = arg.extract_plain_text().split()
    aua_token = config.get_config("aua_token")
    aua_url = config.get_config("aua_url")
    if aua_token == "SECRET" or aua_url == "URL":
        logger.error("ArcaeaUnlimitedApi is not configured!")
        await arc.finish("ArcaeaUnlimitedApi is not configured!")
    if len(args) == 0:
        # Recent
        user_info: UserInfo = UserInfo.get_or_none(UserInfo.user_qq == event.user_id)
        # Expection
        if not user_info:
            await arc.finish(MessageSegment.reply(event.message_id) + "你还没绑定呢！")
        if UserArcaeaInfo.is_querying(user_info.arcaea_id):
            await arc.finish(
                MessageSegment.reply(event.message_id) + "您已在查询队列, 请勿重复发起查询。"
            )
        # Query
        await arc.send(MessageSegment.reply(event.message_id) + "开始查询您最近的游玩记录中，请稍后...")
        user_config = UserUIConfig().read().get(str(event.user_id))
        language = user_config.get("language") if user_config else None
        ui = user_config.get("ui") if user_config else None
        result = await UserArcaeaInfo.draw_user_recent(
            arcaea_id=user_info.arcaea_id, language=language, ui=ui
        )
        await arc.finish(MessageSegment.reply(event.message_id) + result)
