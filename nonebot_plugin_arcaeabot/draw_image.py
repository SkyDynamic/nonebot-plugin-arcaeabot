from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.log import logger
from .adapters.utils import adapter_selector
from .image_generator import draw_b30, draw_recent, draw_user_best
from io import BytesIO

api_in_use = adapter_selector().upper()
if api_in_use == "AUA":
    logger.info("将使用ArcaeaUnlimitedApi")
    from .adapters.aua.resolver import ApiResult
    from .adapters.aua.api import get_user_best
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
            if data.retcode != 0:
                UserArcaeaInfo.querying.remove(arcaea_id)
                return data.message
            else:
                UserArcaeaInfo.querying.remove(arcaea_id)
                image = draw_b30(arcaea_id=arcaea_id, data=data)
                buffer = BytesIO()
                image.save(buffer, "png")
                return MessageSegment.image(buffer)
        except Exception as e:
            UserArcaeaInfo.querying.remove(arcaea_id)
            return str(e)

    @staticmethod
    async def draw_recent_image(arcaea_id: str):
        UserArcaeaInfo.querying.append(arcaea_id)
        try:
            data = ApiResult()
            await data.get_recent(arcaea_id=arcaea_id)
            if data.retcode != 0:
                UserArcaeaInfo.querying.remove(arcaea_id)
                return data.message
            else:
                UserArcaeaInfo.querying.remove(arcaea_id)
                image = draw_recent(arcaea_id=arcaea_id, data=data)
                buffer = BytesIO()
                image.save(buffer, "png")
                return MessageSegment.image(buffer)
        except Exception as e:
            UserArcaeaInfo.querying.remove(arcaea_id)
            return str(e)
    @staticmethod
    async def draw_best(arcaea_id: str, song_id: str):
        UserArcaeaInfo.querying.append(arcaea_id)
        try:
            data = await get_user_best(arcaea_id=arcaea_id, song_id=song_id, difficulty="ftr")
            if data["retcode"] != 0:
                UserArcaeaInfo.querying.remove(arcaea_id)
                return data["message"]
            else:
                UserArcaeaInfo.querying.remove(arcaea_id)
                image = draw_user_best(data=data)
                buffer = BytesIO()
                image.save(buffer, "png")
                return MessageSegment.image(buffer)
        except Exception as e:
            UserArcaeaInfo.querying.remove(arcaea_id)
            return str(e)