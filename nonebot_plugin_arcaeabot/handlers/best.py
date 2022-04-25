from loguru import logger
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, MessageSegment
from nonebot.params import CommandArg
from nonebot.exception import ActionFailed
from nonebot.log import logger
from ..data import UserInfo
from ..main import arc
from ..draw_image import UserArcaeaInfo
from ..database import alias


async def best_handler(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    args: list = str(args).split()
    if args[0] == "best":
        if len(args) == 3:
            user_info = UserInfo.get_or_none(UserInfo.user_qq == event.user_id)
            song_alias = (
                alias.get_or_none(alias.alias == args[1].strip())
                if alias.get_or_none(alias.alias == args[1].strip())
                else alias.get_or_none(alias.sid == args[1].strip())
            )
            song_id = song_alias.sid if song_alias else args[1].strip()
            difficulty = args[2].strip()
            # Exception
            if not user_info:
                try:
                    await arc.finish(
                        "\n".join(
                            [f"> {event.sender.card or event.sender.nickname}", "你还没绑定哦~"]
                        )
                    )
                except ActionFailed as e:
                    logger.exception(
                        f'ActionFailed | {e.info["msg"].lower()} | retcode = {e.info["retcode"]} | {e.info["wording"]}'
                    )
                    return

            # Query
            if not UserArcaeaInfo.is_querying(user_info.arcaea_id):
                result = await UserArcaeaInfo.draw_best(
                    arcaea_id=user_info.arcaea_id, song_id=song_id, difficulty=difficulty
                )
                try:
                    await arc.finish(MessageSegment.reply(event.message_id) + result)
                except ActionFailed as e:
                    logger.exception(
                        f'ActionFailed | {e.info["msg"].lower()} | retcode = {e.info["retcode"]} | {e.info["wording"]}'
                    )
                    return
            else:
                try:
                    await arc.finish(
                        "\n".join(
                            [
                                f"> {event.sender.card or event.sender.nickname}",
                                "您已在查询队列, 请勿重复发起查询。",
                            ]
                        )
                    )
                except ActionFailed as e:
                    logger.exception(
                        f'ActionFailed | {e.info["msg"].lower()} | retcode = {e.info["retcode"]} | {e.info["wording"]}'
                    )
                    return
        else:
            arc.finish("参数输入有误！")