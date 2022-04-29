from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, MessageSegment
from nonebot.params import CommandArg
from ..main import arc
from ..draw_text import draw_song
from .._RHelper import RHelper
import json

root = RHelper()


async def song_handler(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    args: list = str(args).split()
    if args[0] == "song" or args[0] == "songs":

        slst_json = root.assets / ("slst.json")
        with open(slst_json, "r") as file:
            data = json.load(file)

        song = "no_song"
        for s in data["songs"]:
            if s["song_id"] == args[1].strip():
                song = s
            if s["difficulties"][0]["name_en"] == args[1].strip() or s["difficulties"][0]["name_jp"] == args[1].strip():
                song = s
            if len(s["difficulties"]) == 4:
                if s["difficulties"][3]["name_en"] == args[1].strip() or s["difficulties"][3]["name_jp"] == args[1].strip():
                    song = s
            for alias in s["alias"]:
                if alias == args[1].strip():
                    song = s
                    
        # check
        if song == "no_song":
            await arc.finish(MessageSegment.reply(event.message_id) + "曲目不存在！")
        if len(args) == 2:
            difficulty = "all"
        elif len(args) != 3:
            await arc.finish(MessageSegment.reply(event.message_id) + "不支持的命令参数")
        elif args[2].strip().lower() == "byd":
            if len(song["difficulties"]) == 3:
                await arc.finish(MessageSegment.reply(event.message_id) + "难度不存在！")
            difficulty = "3"
        elif args[2].strip().lower() == "ftr":
            difficulty = "2"
        elif args[2].strip().lower() == "prs":
            difficulty = "1"
        elif args[2].strip().lower() == "pst":
            difficulty = "0"
        else:
            await arc.finish(MessageSegment.reply(event.message_id) + "参数输入有误！")

        await arc.finish(MessageSegment.reply(event.message_id) + draw_song(song_info=song, difficulty=difficulty))
