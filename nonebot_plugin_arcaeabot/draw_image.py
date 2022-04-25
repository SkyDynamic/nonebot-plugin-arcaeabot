from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.log import logger
from .image_generator import draw_b30, draw_recent, draw_user_best
from io import BytesIO
from .request import get_user_best, fetch_user_info


class UserArcaeaInfo:
    querying = list()

    @staticmethod
    def is_querying(arcaea_id: str) -> bool:
        return arcaea_id in UserArcaeaInfo.querying

    @staticmethod
    async def draw_best30_image(arcaea_id: str):
        UserArcaeaInfo.querying.append(arcaea_id)
        try:
            data = await fetch_user_info(arcaea_id=arcaea_id)
            if data["status"] != 0:
                UserArcaeaInfo.querying.remove(arcaea_id)
                return data["message"]
            else:
                UserArcaeaInfo.querying.remove(arcaea_id)
                image = draw_b30(data=data)
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
            data = await fetch_user_info(arcaea_id=arcaea_id, recent_only=True)
            if data["status"] != 0:
                UserArcaeaInfo.querying.remove(arcaea_id)
                return data["message"]
            else:
                UserArcaeaInfo.querying.remove(arcaea_id)
                image = draw_recent(data=data)
                buffer = BytesIO()
                image.save(buffer, "png")
                return MessageSegment.image(buffer)
        except Exception as e:
            UserArcaeaInfo.querying.remove(arcaea_id)
            return str(e)

    @staticmethod
    async def draw_best(arcaea_id: str, song_id: str, difficulty: str):
        UserArcaeaInfo.querying.append(arcaea_id)
        try:
            data = await get_user_best(
                arcaea_id=arcaea_id, song_id=song_id, difficulty=difficulty
            )
            if data["status"] != 0:
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
