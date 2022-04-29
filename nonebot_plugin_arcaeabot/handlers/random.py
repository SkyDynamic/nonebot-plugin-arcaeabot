import random
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, MessageSegment
from nonebot.params import CommandArg
from ..main import arc
from ..draw_text import draw_song
from .._RHelper import RHelper
import json

root = RHelper()


async def random_handler(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    args: list = str(args).split()
    if args[0] == "random":
        with open(root.assets / "slst.json", "r", encoding="UTF-8") as f:
            slst = json.loads(f.read())
        min: int = 0
        max: int = 1150

        if len(args) == 2:
            min = float(args[1].strip()) * 10
            max = float(args[1].strip()) * 10

        if len(args) == 3:
            min = float(args[1].strip()) * 10
            max = float(args[2].strip()) * 10

        n = 0
        for s in slst["songs"]:
            for l in s["difficulties"]:
                if l["rating"] >= min and l["rating"] <= max:
                    n = n + 1
                    break
        n = random.randint(0, n - 1)
        for s in slst["songs"]:
            for l in s["difficulties"]:
                if l["rating"] >= min and l["rating"] <= max:
                    if n == 0:
                        song = s
                    n = n - 1
                    break

        await arc.finish(MessageSegment.reply(event.message_id) + draw_song(song_info=song))
