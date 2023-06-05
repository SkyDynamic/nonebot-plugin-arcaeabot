from nonebot.adapters.onebot.v11 import MessageEvent, Message, MessageSegment
from nonebot.params import CommandArg
from ..matcher import arc
from ..message.text_message import TextMessage
from ..api.request import API
from ..config import StatusMsgDict


async def random_handler(event: MessageEvent, arg: Message = CommandArg()):
    args = arg.extract_plain_text().split()
    args = {i: v for i, v in enumerate(args)}
    if args.get(0, None) == "random" or args.get(0, None) == "rd":
        # get args
        start = args.get(1, "0")
        end = args.get(2, "20")
        resp = await API.get_song_random(start=start, end=end)
        if resp.message:
            await arc.finish(
                MessageSegment.reply(event.message_id) + StatusMsgDict.get(str(resp.status))
                )
        await arc.finish(
            MessageSegment.reply(event.message_id) + TextMessage.song_info_detail(resp)
        )
