from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from nonebot.exception import ActionFailed
from nonebot.params import CommandArg
from nonebot.log import logger
from ..data import UserInfo
from ..matcher import arc
from ..AUA import get_user_info


async def bind_handler(bot: Bot, event: MessageEvent, args=CommandArg()):
    args: list = str(args).split()
    if args[0] == "bind":
        arc_id = args[1].strip()
        if len(arc_id) != 9:
            try:
                await arc.finish(
                    "\n".join(
                        [
                            f"> {event.sender.card or event.sender.nickname}",
                            "id 格式错误，请检查。",
                        ]
                    )
                )
            except ActionFailed as e:
                logger.exception(
                    f'ActionFailed | {e.info["msg"].lower()} | retcode = {e.info["retcode"]} | {e.info["wording"]}'
                )
        res1 = await get_user_info(arcaea_id=arc_id)
        if res1["status"] != 0:
            return str(res1["status"]) + ": " + res1["message"]
        player_name = res1["content"]["account_info"]["name"]
        UserInfo.replace(
            user_qq=event.user_id, arcaea_id=arc_id, arcaea_name=player_name
        ).execute()
        try:
            await arc.finish(
                "\n".join(
                    [
                        f"> {event.sender.card or event.sender.nickname}",
                        f"绑定成功, 用户名: {player_name}, id: {arc_id}",
                    ]
                )
            )
        except ActionFailed as e:
            logger.exception(
                f'ActionFailed | {e.info["msg"].lower()} | retcode = {e.info["retcode"]} | {e.info["wording"]}'
            )
