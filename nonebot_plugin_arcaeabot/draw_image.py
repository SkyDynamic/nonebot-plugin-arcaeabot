from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.log import logger
from .assets import StaticPath
from .adapters.utils import adapter_selector
from .image_generator import draw_b30, draw_recent

api_in_use = adapter_selector().upper()
if api_in_use == "AUA":
    logger.info("将使用ArcaeaUnlimitedApi")
    from .adapters.aua.resolver import ApiResult
elif api_in_use == "ESTERTION":
    logger.info("将使用EstertionApi")
    from .adapters.estertion.resolver import ApiResult
else:
    logger.error("不支持的Api选项")


class UserArcaeaInfo:
    querying = list()

    @staticmethod
    def is_querying(arcaea_id: str) -> bool:
        return arcaea_id in UserArcaeaInfo.querying

    @staticmethod
    async def draw_best30_image(arcaea_id: str):
        UserArcaeaInfo.querying.append(arcaea_id)
        try:
            data = ApiResult()
            await data.get_b30(arcaea_id=arcaea_id)
        except Exception as e:
            UserArcaeaInfo.querying.remove(arcaea_id)
            return str(e)
        UserArcaeaInfo.querying.remove(arcaea_id)
        image = draw_b30(arcaea_id=arcaea_id, data=data)
        image.save(StaticPath.output(str(arcaea_id)))
        return MessageSegment.image("file:///"+StaticPath.output(str(arcaea_id)))

    @staticmethod
    async def draw_recent_image(arcaea_id: str):
        UserArcaeaInfo.querying.append(arcaea_id)
        try:
            data = ApiResult()
            await data.get_recent(arcaea_id=arcaea_id)
        except Exception as e:
            UserArcaeaInfo.querying.remove(arcaea_id)
            return str(e)
        UserArcaeaInfo.querying.remove(arcaea_id)
        image = draw_recent(arcaea_id=arcaea_id, data=data)
        image.save(StaticPath.output(str(arcaea_id) + "_recent"))
        return MessageSegment.image("file:///"+StaticPath.output(str(arcaea_id) + "_recent"))
