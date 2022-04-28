from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, MessageSegment
from nonebot.params import CommandArg
from ..matcher import arc
from ..assets_updater import check_song_update, check_char_update
from os import remove, path
from .._RHelper import RHelper
from shutil import rmtree

root = RHelper()


async def assets_update_handler(
    bot: Bot, event: MessageEvent, args: Message = CommandArg()
):
    args: list = str(args).split()
    if args[0] == "assets_update":

        if len(args) == 2 and args[1] == 'all':
            if path.exist(root.assets.song):
                rmtree(root.assets.song)
            if path.exist(root.assets.char):
                rmtree(root.assets.char)
            if path.exist(root.assets / ("slst.json")):
                remove(root.assets / ("slst.json"))
        elif len(args) != 1:
            await arc.finish(MessageSegment.reply(event.message_id) + "不支持的命令参数")

        await arc.send("正在更新，请关注控制台更新进度…")
        result_song = await check_song_update()
        result_char = await check_char_update()

        await arc.finish(
            MessageSegment.reply(event.message_id) +
            "\n".join(
                [
                    f"成功更新 {len(result_song)} 张曲绘, ",
                    f"成功更新 {len(result_char)} 张立绘",
                ]
            )
        )