from ..config import UserUIConfig
from ..matcher import arc

from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.params import CommandArg


async def ui_handler(event: MessageEvent, arg: Message = CommandArg()):
    args = arg.extract_plain_text().split()
    reply = MessageSegment.reply(event.message_id)
    if args[0] == "ui":
        if len(args) == 3:
            config = UserUIConfig()
            origin_data = config.read()
            if args[1] in ["语言", "lang", "language"]:
                if args[2] in ["英文", "en", "english"]:
                    if not origin_data.get(str(event.user_id)):
                        origin_data[str(event.user_id)] = {"language": "en", "ui": 0}
                    else:
                        origin_data[str(event.user_id)]["language"] = "en"
                    config.write(origin_data)
                    await arc.finish(reply + "生成图片的语言已更换为English")
                elif args[2] in ["日文", "jp", "japanese"]:
                    if not origin_data.get(str(event.user_id)):
                        origin_data[str(event.user_id)] = {"language": "jp", "ui": 0}
                    else:
                        origin_data[str(event.user_id)]["language"] = "jp"
                    config.write(origin_data)
                    await arc.finish(reply + "生成图片的语言已更换为Janpanese")
                else:
                    await arc.finish(reply + "参数不存在")
            elif args[1] in ["样式", "style", "ui"]:
                if args[2] == "0":
                    if not origin_data.get(str(event.user_id)):
                        origin_data[str(event.user_id)] = {"language": "en", "ui": 0}
                    else:
                        origin_data[str(event.user_id)]["ui"] = 0
                    config.write(origin_data)
                    await arc.finish(reply + "生成图片的样式已改为Andrea_Style_v3")
                if args[2] == "1":
                    if not origin_data.get(str(event.user_id)):
                        origin_data[str(event.user_id)] = {"language": "en", "ui": 1}
                    else:
                        origin_data[str(event.user_id)]["ui"] = 1
                    config.write(origin_data)
                    await arc.finish(reply + "生成图片的样式已改为Arcaea_Style_v1")
        else:
            await arc.finish(reply + "缺少参数")
