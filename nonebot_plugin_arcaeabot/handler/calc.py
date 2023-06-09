from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.params import CommandArg

from ..message.text_message import CalcMessage
from ..api.request import API
from ..config import StatusMsgDict
from ..schema import diffstr2num
from ..matcher import arc

helpmsg = '''计算器使用方法：

分数推算单曲Ptt:
/arc calc ptt <单曲分数> <Arc 曲目> [Arc 难度等级]
例如: /arc calc ptt 9832152 Grievous Lady ftr

单曲Ptt推算分数:
/arc calc score <单曲 Ptt> <Arc 曲目> [Arc 难度等级]
例如: /arc calc score 11.3 Grievous Lady ftr

注：例子中的命令前缀为默认前缀，请按实际情况更改
'''

async def calc_handler(event: MessageEvent, arg: Message = CommandArg()):
    args = arg.extract_plain_text().split()
    reply = MessageSegment.reply(event.message_id)
    if args[0] == 'calc':
        if len(args) == 1:
            await arc.finish(
                reply + helpmsg
            )
        try:
            if len(args) > 2:
                if args[1] in ['score', 'ptt']:
                    '''/arc calc score 11.3 Grievous Lady ftr'''
                    if len(args) >= 4 and args[1] == 'score':
                        ptt = float(args[2])
                        difficulty = diffstr2num(args[-1].upper())
                        if difficulty:
                            songname = args[3:-1]
                        else:
                            difficulty = 2
                            songname = " ".join(args[3:])
                        resp = await API.get_song_info(songname=songname)
                        if resp.message:
                            await arc.finish(
                                MessageSegment.reply(event.message_id) + StatusMsgDict.get(str(resp.status))
                                )
                        result = CalcMessage.score(resp, ptt, difficulty)
                        await arc.finish(
                            reply + result
                            )
                    '''/arc calc ptt 9832152 Grievous Lady ftr'''
                    if len(args) >= 4 and args[1] == 'ptt':
                        score = int(args[2])
                        difficulty = diffstr2num(args[-1].upper())
                        if difficulty:
                            songname = args[3:-1]
                        else:
                            difficulty = 2
                            songname = " ".join(args[3:])
                        resp = await API.get_song_info(songname=songname)
                        if resp.message:
                            await arc.finish(
                                MessageSegment.reply(event.message_id) + StatusMsgDict.get(str(resp.status))
                                )
                        result = CalcMessage.ptt(resp, score, difficulty)
                        await arc.finish(
                            reply + result
                            )
                else:
                    await arc.finish(
                        reply + StatusMsgDict.get("-1002")
                    )
        except Exception as e:
            await arc.finish(
                reply + str(e)
            )