from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
from nonebot.params import CommandArg
from ..data import UserInfo
from ..matcher import arc
from ..request import get_user_info


async def bind_handler(bot: Bot, event: MessageEvent, args=CommandArg()):
    args: list = str(args).split()

    if args[0] == "bind":
        arc_id = args[1].strip()

        # Expection
        if len(args) != 2:
            await arc.finish(MessageSegment.reply(event.message_id) + "不支持的命令参数")

        if len(arc_id) != 9:
            await arc.finish(MessageSegment.reply(event.message_id) + "id 格式错误！")

        # Query
        res1 = await get_user_info(arcaea_id=arc_id)
        if res1["status"] != 0:
            await arc.finish(str(res1["status"]) + ": " + res1["message"])
        player_name = res1["content"]["account_info"]["name"]
        UserInfo.replace(
            user_qq=event.user_id, arcaea_id=arc_id, arcaea_name=player_name
        ).execute()

        await arc.finish(MessageSegment.reply(event.message_id) + f"绑定成功, 用户名: {player_name}, id: {arc_id}")
