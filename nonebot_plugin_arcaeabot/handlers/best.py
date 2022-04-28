from os import ftruncate
from loguru import logger
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, MessageSegment
from nonebot.params import CommandArg
from nonebot.exception import ActionFailed
from ..data import UserInfo
from ..main import arc
from ..draw_image import UserArcaeaInfo
from .._RHelper import RHelper
import json

root = RHelper()


async def best_handler(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    args: list = str(args).split()
    if args[0] == "best":
        user_info = UserInfo.get_or_none(UserInfo.user_qq == event.user_id)
        '''
        song_alias = (
            alias.get_or_none(alias.alias == args[1].strip())
            if alias.get_or_none(alias.alias == args[1].strip())
            else alias.get_or_none(alias.sid == args[1].strip())
        )
        song_id = song_alias.sid if song_alias else args[1].strip()
        '''
        slst_json = root.assets / ("slst.json")
        with open(slst_json, "r") as file:
            data = json.load(file)

        for s in data["content"]["songs"]:
            if s["song_id"] == args[1].strip():
                song_id = s["song_id"]
                song = s
            for alias in s["alias"]:
                if alias == args[1].strip():
                    song_id = s["song_id"]
                    song = s
                    
        # check
        if len(args) == 2:
            difficulty = 2
        elif len(args) != 3:
            await arc.finish("参数输入长度有误！")
        elif args[2].strip().lower() == "byd":
            difficulty = 3
        elif args[2].strip().lower() == "ftr":
            difficulty = 2
        elif args[2].strip().lower() == "prs":
            difficulty = 1
        elif args[2].strip().lower() == "pst":
            difficulty = 0
        else:
            await arc.finish("参数输入有误！")

        if not song["difficulties"][difficulty]:
            await arc.finish("难度不存在！")
            
        # Exception
        if not user_info:
            await arc.finish(
                "\n".join(
                    [
                        f"> {event.sender.card or event.sender.nickname}",
                        "你还没绑定哦~",
                    ]
                )
            )
        # Query
        if not UserArcaeaInfo.is_querying(user_info.arcaea_id):
            result = await UserArcaeaInfo.draw_best(
                arcaea_id=user_info.arcaea_id,
                song_id=song_id,
                difficulty=difficulty,
            )
            await arc.finish(MessageSegment.reply(event.message_id) + result)

        else:
            await arc.finish(
                "\n".join(
                    [
                        f"> {event.sender.card or event.sender.nickname}",
                        "您已在查询队列, 请勿重复发起查询。",
                    ]
                )
            )
