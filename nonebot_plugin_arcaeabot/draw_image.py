from nonebot.adapters.onebot.v11 import MessageSegment
from . import image_generator
from io import BytesIO
from .AUA import get_user_best, get_user_b30, get_user_recent


class UserArcaeaInfo:
    querying = list()

    @staticmethod
    def is_querying(arcaea_id: str) -> bool:
        return arcaea_id in UserArcaeaInfo.querying

    @staticmethod
    async def draw_user_b30(arcaea_id: str):
        UserArcaeaInfo.querying.append(arcaea_id)
        try:
            data = await get_user_b30(arcaea_id=arcaea_id, overflow=10)
            if data["status"] != 0:
                UserArcaeaInfo.querying.remove(arcaea_id)
                return str(data["status"]) + ": " + data["message"]
            else:
                image = image_generator.draw_user_b30(data=data["content"])
                buffer = BytesIO()
                image.save(buffer, "png")
                UserArcaeaInfo.querying.remove(arcaea_id)
                return MessageSegment.image(buffer)
        except Exception as e:
            UserArcaeaInfo.querying.remove(arcaea_id)
            return str(e)

    @staticmethod
    async def draw_user_recent(arcaea_id: str):
        UserArcaeaInfo.querying.append(arcaea_id)
        try:
            data = await get_user_recent(arcaea_id=arcaea_id)
            if data["status"] != 0:
                UserArcaeaInfo.querying.remove(arcaea_id)
                return str(data["status"]) + ": " + data["message"]
            else:
                image = image_generator.draw_user_recent(data=data["content"])
                buffer = BytesIO()
                image.save(buffer, "png")
                UserArcaeaInfo.querying.remove(arcaea_id)
                return MessageSegment.image(buffer)
        except Exception as e:
            UserArcaeaInfo.querying.remove(arcaea_id)
            return str(e)

    @staticmethod
    async def draw_user_best(arcaea_id: str, song_id: str, difficulty: str):
        UserArcaeaInfo.querying.append(arcaea_id)
        try:
            data = await get_user_best(arcaea_id=arcaea_id, song_id=song_id, difficulty=difficulty)
            if data["status"] != 0:
                UserArcaeaInfo.querying.remove(arcaea_id)
                return str(data["status"]) + ": " + data["message"]
            else:
                image = image_generator.draw_user_best(data=data["content"])
                buffer = BytesIO()
                image.save(buffer, "png")
                UserArcaeaInfo.querying.remove(arcaea_id)
                return MessageSegment.image(buffer)
        except Exception as e:
            UserArcaeaInfo.querying.remove(arcaea_id)
            return str(e)

