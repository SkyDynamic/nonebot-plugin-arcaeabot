from .best_30.chieri_style import draw_user_b30, draw_ptt
from .single_song.andreal_style_v3 import draw_single_song
from .single_song import arcaea_style_v2
from ...api.request import API
from typing import Optional
from io import BytesIO
from nonebot.adapters.onebot.v11.message import MessageSegment


class UserArcaeaInfo:
    querying = list()

    @staticmethod
    def is_querying(arcaea_id: str) -> bool:
        return arcaea_id in UserArcaeaInfo.querying

    @staticmethod
    async def draw_user_b30(language: str, arcaea_id: str):
        UserArcaeaInfo.querying.append(arcaea_id)
        try:
            session_get = await API.get_user_session(arcaea_id=arcaea_id)
            if content := session_get.content:
                if session_info := content.session_info:
                    resp = await API.get_user_b30(session_info=session_info)
                else:
                    return session_get.message
            else:
                return session_get.message
            if error_message := resp.message:
                return error_message
            image = draw_user_b30(data=resp, language=language)
            buffer = BytesIO()
            image.convert("RGB").save(buffer, "jpeg")
            return MessageSegment.image(buffer)
        except Exception as e:
            return str(e)
        finally:
            UserArcaeaInfo.querying.remove(arcaea_id)

    @staticmethod
    async def draw_user_ptt(arcaea_id: str):
        UserArcaeaInfo.querying.append(arcaea_id)
        try:
            session_get = await API.get_user_session(arcaea_id=arcaea_id)
            if content := session_get.content:
                if session_info := content.session_info:
                    resp = await API.get_user_b30(session_info=session_info)
                else:
                    return session_get.message
            else:
                return session_get.message
            if error_message := resp.message:
                return error_message
            image = draw_ptt(data=resp)
            buffer = BytesIO()
            image.convert("RGB").save(buffer, "jpeg")
            return MessageSegment.image(buffer)
        except Exception as e:
            return str(e)
        finally:
            UserArcaeaInfo.querying.remove(arcaea_id)

    @staticmethod
    async def draw_user_recent(arcaea_id: str, language: str, ui: Optional[int]):
        UserArcaeaInfo.querying.append(arcaea_id)
        try:
            resp = await API.get_user_info(arcaea_id=arcaea_id)
            if error_message := resp.message:
                return error_message
            if ui == 0 or not ui:
                image = draw_single_song(data=resp, language=language)
            elif ui == 1:
                image = arcaea_style_v2.draw_single_song(data=resp, language=language)
            buffer = BytesIO()
            image.convert("RGB").save(buffer, "jpeg")
            return MessageSegment.image(buffer)
        except Exception as e:
            return str(e)
        finally:
            UserArcaeaInfo.querying.remove(arcaea_id)

    @staticmethod
    async def draw_user_best(
        arcaea_id: str, songname: str, difficulty: int, language: str, ui: Optional[int]
    ):
        UserArcaeaInfo.querying.append(arcaea_id)
        try:
            resp = await API.get_user_best(
                arcaea_id=arcaea_id, songname=songname, difficulty=difficulty
            )
            if error_message := resp.message:
                return error_message
            if ui == 0 or not ui:
                image = draw_single_song(data=resp, language=language)
            elif ui == 1:
                image = arcaea_style_v2.draw_single_song(data=resp, language=language)
            buffer = BytesIO()
            image.convert("RGB").save(buffer, "jpeg")
            return MessageSegment.image(buffer)
        except Exception as e:
            return str(e)
        finally:
            UserArcaeaInfo.querying.remove(arcaea_id)
