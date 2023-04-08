from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.params import CommandArg
from ..api.request import API
from ..message.text_message import TextMessage
from ..matcher import arc

async def ai_handler(event: MessageEvent, arg: Message = CommandArg()):
    args = arg.extract_plain_text().split()
    if args[0] == "ai":
        resp = await API.get_song_random(start='0', end='24')
        if error_message := resp.message:
            await arc.finish(
                MessageSegment.reply(event.message_id) + error_message
            )
        await arc.finish(
            MessageSegment.reply(event.message_id) + TextMessage.ai_song_info_detail(resp)
        )