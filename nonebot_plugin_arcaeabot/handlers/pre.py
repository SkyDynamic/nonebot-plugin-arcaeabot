from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message
from nonebot.params import CommandArg
from ..matcher import arc
from ..config import config


async def pre_handler(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    args: list = str(args).split()
    if len(args) == 0:
        await arc.finish(
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
    elif args[0] not in [
        "help",
        "info",
        "recent",
        "b30",
        "bind",
        "unbind",
        "assets_update",
        "best",
    ]:
        await arc.finish("不支持的命令参数")
    else:
        aua_ua = config.get_config("aua_ua")
        aua_url = config.get_config("aua_url")
        if aua_ua == "SECRET" or aua_url == "URL":
            await arc.finish("ArcaeaUnlimitedApi is not configured!")
