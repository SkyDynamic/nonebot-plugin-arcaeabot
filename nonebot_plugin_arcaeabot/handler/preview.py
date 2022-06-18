from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, MessageSegment
from nonebot.params import CommandArg
from ..matcher import arc
from ..api.request import API
from ..schema import diffstr2num
from io import BytesIO


async def preview_handler(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    """
    /arc preview Fracture Ray ftr
    """
    args = arg.extract_plain_text().split()
    if len(args) >= 2 and args[0] == "preview":
        # get args
        if difficulty := diffstr2num(args[-1].upper()):
            songname = " ".join(args[1:-1])
        else:
            difficulty = 2
            songname = " ".join(args[1:])
        # query
        resp = await API.get_song_preview(songname=songname, difficulty=difficulty)
        await arc.finish(
            MessageSegment.reply(event.message_id) + MessageSegment.image(resp)
        )
