from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, MessageSegment
from nonebot.params import CommandArg
from ..matcher import arc


async def help_handler(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    args: list = str(args).split()
    if args[0] == "help":
        await arc.finish(
            MessageSegment.reply(event.message_id) +
            "\n".join(
                [
                    "/arc bind {arcaea id} 进行绑定。",
                    "/arc unbind 解除绑定。",
                    "/arc info 查看绑定信息。",
                    "/arc recent 查询上一次游玩记录。",
                    "/arc b30 查询 best 30 记录。",
                    "/arc assets_update 更新曲绘与立绘资源",
                    r"/arc best {songname} {difficulty} 查询单曲最高分",
                ]
            )
        )
