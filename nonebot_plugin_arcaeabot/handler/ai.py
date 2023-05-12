from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.params import CommandArg
from nonebot.params import ArgPlainText
from nonebot.matcher import Matcher
from ..api.request import API
from ..matcher import arc, ai_cmd
from ..message.text_message import TextMessage

from apscheduler.schedulers.background import BackgroundScheduler

import time

Ai_query_reset_scheduler = BackgroundScheduler()

first_msg = (
    "您好!我是Ai酱，出身于韵律源点Arcaea"
    "的一位内置人工智能助手。众所周知，打音游的时候要进入状态才能发挥得好。因此，每当不确定要玩哪首歌曲时，您都可以来问我，我会推荐一些曲目来帮助您进入状态，并同时体会到游玩的乐趣!"
)


async def ai_handler(
    event: MessageEvent, matcher: Matcher, arg: Message = CommandArg()
):
    reply = MessageSegment.reply(event.message_id)
    specific_number = TextMessage.query_data.get(str(event.user_id))
    await arc.send(
        reply
        + first_msg
        + f'\n剩余请求次数：{specific_number.get("specific_number") if specific_number else 5}'
        + "\n\n1: 推荐一首歌给我吧\n2: 结束会话(不需要请务必回复此代码否侧返回未知参数)\n(输入数字代码，不要输入其他的)"
    )
    matcher.stop_propagation()


async def ai_first_handler(event: MessageEvent, code: str = ArgPlainText("code")):
    reply = MessageSegment.reply(event.message_id)
    if code == "1":
        resp = await random(event)
        await arc.send(
            reply
            + TextMessage.ai_song_info_detail(resp, str(event.user_id))
            + "\n\n1: 再推荐一首歌给我吧!\n2: 好耶, 冲冲冲!\n3: 结束会话("
            "不需要请务必回复此代码否侧返回未知参数)\n(输入数字代码，不要输入其他的)"
        )
    elif code == "2":
        await arc.finish(reply + "会话结束")


async def ai_continue_handler(event: MessageEvent, code: str = ArgPlainText("code_")):
    reply = MessageSegment.reply(event.message_id)
    if code == "1":
        resp = await random(event)
        await arc.reject(
            reply
            + TextMessage.ai_song_info_detail(resp, str(event.user_id))
            + "\n\n1: 再推荐一首歌给我吧!\n2: 好耶, 冲冲冲!\n3: 结束会话("
            "不需要请务必回复此代码否侧返回未知参数)\n(输入数字代码，不要输入其他的)"
        )
    elif code == "2":
        await arc.reject(
            reply
            + TextMessage.song_info_detail(
                TextMessage.query_data[str(event.user_id)]["resp"]
            )
            + "\n\n1: 再推荐一首歌给我吧!\n2: 好耶, 冲冲冲!\n3: 结束会话("
            "不需要请务必回复此代码否侧返回未知参数)\n(输入数字代码，不要输入其他的)"
        )
    elif code == "3":
        await arc.finish(reply + "会话结束")


@Ai_query_reset_scheduler.scheduled_job("interval", seconds=60)
def Ai_query_reset_handler():
    now = int(time.time())
    data = TextMessage.query_data
    for i in data:
        if data[i]["reset_time"] and now >= data[i]["reset_time"]:
            data[i]["reset_time"] = None
            data[i]["specific_number"] = 5
    TextMessage.query_data = data


async def random(event: MessageEvent):
    reply = MessageSegment.reply(event.message_id)
    resp = await API.get_song_random(start="0", end="24")
    if error_message := resp.message:
        await arc.finish(reply + error_message)
    return resp
