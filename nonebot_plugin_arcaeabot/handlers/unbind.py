from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, MessageSegment
from nonebot.params import CommandArg
from ..matcher import arc
from ..data import UserInfo


async def unbind_handler(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    args: list = str(args).split()
    if args[0] == "unbind":
        user_info = UserInfo.get_or_none(UserInfo.user_qq == event.user_id)

        # Expection
        if len(args) != 1:
            await arc.finish(MessageSegment.reply(event.message_id) + "不支持的命令参数")

        if not user_info:
            await arc.finish(MessageSegment.reply(event.message_id) + "你还没绑定呢！")

        UserInfo.delete().where(UserInfo.user_qq == event.user_id).execute()
        await arc.finish(MessageSegment.reply(event.message_id) + "已成功删除用户记录。")
