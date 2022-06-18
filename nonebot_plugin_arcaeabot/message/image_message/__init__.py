from .best_30.chieri_style import draw_user_b30
from .single_song.andreal_style_v3 import draw_single_song
from ...api.request import API
from io import BytesIO
from nonebot.adapters.onebot.v11.message import MessageSegment


class UserArcaeaInfo:
    querying = list()

    @staticmethod
    def is_querying(arcaea_id: str) -> bool:
        return arcaea_id in UserArcaeaInfo.querying

    @staticmethod
    async def draw_user_b30(arcaea_id: str):
        UserArcaeaInfo.querying.append(arcaea_id)
        try:
            resp = await API.get_user_b30(arcaea_id=arcaea_id)
            if error_message := resp.message:
                return error_message
            image = draw_user_b30(data=resp)
            buffer = BytesIO()
            image.save(buffer, "png")
            return MessageSegment.image(buffer)
        except Exception as e:
            return str(e)
        finally:
            UserArcaeaInfo.querying.remove(arcaea_id)

    @staticmethod
    async def draw_user_recent(arcaea_id: str):
        UserArcaeaInfo.querying.append(arcaea_id)
        try:
            resp = await API.get_user_info(arcaea_id=arcaea_id)
            if error_message := resp.message:
                return error_message
            image = draw_single_song(data=resp)
            buffer = BytesIO()
            image.save(buffer, "png")
            return MessageSegment.image(buffer)
        except Exception as e:
            return str(e)
        finally:
            UserArcaeaInfo.querying.remove(arcaea_id)

    @staticmethod
    async def draw_user_best(arcaea_id: str, songname: str, difficulty: int):
        UserArcaeaInfo.querying.append(arcaea_id)
        try:
            resp = await API.get_user_best(
                arcaea_id=arcaea_id, songname=songname, difficulty=difficulty
            )
            if error_message := resp.message:
                return error_message
            image = draw_single_song(data=resp)
            buffer = BytesIO()
            image.save(buffer, "png")
            return MessageSegment.image(buffer)
        except Exception as e:
            return str(e)
        finally:
            UserArcaeaInfo.querying.remove(arcaea_id)
