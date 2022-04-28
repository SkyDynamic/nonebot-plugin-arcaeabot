from os import ftruncate
from loguru import logger
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, MessageSegment
from nonebot.params import CommandArg
from nonebot.exception import ActionFailed
from ..data import UserInfo, alias
from ..main import arc
from ..draw_image import UserArcaeaInfo


async def best_handler(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    args: list = str(args).split()
    if args[0] == "best":
        user_info = UserInfo.get_or_none(UserInfo.user_qq == event.user_id)
        song_alias = (
            alias.get_or_none(alias.alias == args[1].strip())
            if alias.get_or_none(alias.alias == args[1].strip())
            else alias.get_or_none(alias.sid == args[1].strip())
        )
        song_id = song_alias.sid if song_alias else args[1].strip()

        # check
        if len(args) == 2:
            difficulty = "ftr"
        elif len(args) != 3:
            await arc.finish("参数输入长度有误！")
        elif (
            args[2].strip().lower() == "byd"
            or args[2].strip().lower() == "ftr"
            or args[2].strip().lower() == "prs"
            or args[2].strip().lower() == "pst"
        ):
            difficulty = args[2].strip()
        elif args[2].strip() >= "0" and args[2].strip() <= "3":
            difficulty = args[2].strip()
        else:
            await arc.finish("参数输入有误！")

        # Exception
        if not user_info:
            try:
                await arc.finish(
                    "\n".join(
                        [
                            f"> {event.sender.card or event.sender.nickname}",
                            "你还没绑定哦~",
                        ]
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
                arcaea_id=user_info.arcaea_id,
                song_id=song_id,
                difficulty=difficulty.lower(),
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
