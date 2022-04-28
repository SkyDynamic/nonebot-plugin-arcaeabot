from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message
from nonebot.params import CommandArg
from nonebot.log import logger
from nonebot.exception import ActionFailed
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

    if len(args) == 2 and args[1] == "all":
        if path.exist(root.assets.song):
            rmtree(root.assets.song)
        if path.exist(root.assets.char):
            rmtree(root.assets.char)
        if path.exist(root.assets / ("slst.json")):
            remove(root.assets / ("slst.json"))

    if args[0] == "assets_update":
        await arc.send("正在更新…")
        result_song = await check_song_update()
        result_char = await check_char_update()
        try:
            await arc.finish(
                "\n".join(
                    [
                        f"> {event.sender.card or event.sender.nickname}",
                        f"成功更新 {len(result_song)} 张曲绘, ",
                        f"成功更新 {len(result_char)} 张立绘",
                    ]
                )
            )
        except ActionFailed as e:
            logger.exception(
                f'ActionFailed | {e.info["msg"].lower()} | retcode = {e.info["retcode"]} | {e.info["wording"]}'
            )
            await arc.finish("更新出错！")
