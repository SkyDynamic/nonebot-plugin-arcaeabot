from httpx import AsyncClient
from websockets.exceptions import *
from ..config import config
from ..schema import (
    UserInfo,
    UserBest30,
    UserBest,
    SongRandom,
    AUASongInfo,
    UserSession,
)
import websockets
import json

aua_url: str = config.get_config("aua_url")
aua_token = config.get_config("aua_token")


def removesuffix(s: str, suffix: str) -> str:
    if suffix and s.endswith(suffix):
        return s[: -len(suffix)]
    else:
        return s[:]


class API:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/104.0.0.0 Safari/537.36",
        "Authorization": f"Bearer {aua_token}",
    }
    # 真正适配Python 3.8
    base_url = removesuffix(aua_url, "/botarcapi/")

    @classmethod
    async def _quick_get(cls, url: str):
        async with AsyncClient(timeout=100) as client:
            resp = await client.get(url=url, headers=cls.headers)
        return resp

    @classmethod
    async def get_user_info(cls, arcaea_id: str):
        url = f"{cls.base_url}/arcapi/user/info?user_name={arcaea_id}&recent=1&with_song_info=true"
        resp = await cls._quick_get(url=url)
        return UserInfo(**resp.json())

    @classmethod
    async def get_user_session(cls, arcaea_id: str):
        url = f"{cls.base_url}/arcapi/user/bests/session?user_code={arcaea_id}"
        resp = await cls._quick_get(url=url)
        return UserSession(**resp.json())

    @classmethod
    async def get_user_b30(cls, session_info: str):
        url = f"{cls.base_url}/arcapi/user/bests/result?session_info={session_info}".replace(
            "https", "wss"
        )
        async with websockets.connect(uri=url, extra_headers=cls.headers) as websocket:
            try:
                package_recv = []
                async for message in websocket:
                    package_recv.append(json.loads(message))
            except ConnectionClosedError as e:
                pass
            finally:
                await websocket.close()
                account_info = package_recv[0]["content"]["account_info"]
                chart_list = package_recv[1:]
                chart_list.sort(
                    key=lambda v: v["content"]["record"]["rating"], reverse=True
                )
                chart_b40 = chart_list[:41]
                score_info_list = [i["content"]["record"] for i in chart_b40]
                song_info_list = [i["content"]["song_info"] for i in chart_b40]
                best_total: float = 0.0
                for i in (
                    range(30)
                    if len(score_info_list) >= 30
                    else range(len(score_info_list))
                ):
                    best_total += score_info_list[i]["rating"]
                best30_avg = best_total / 30
                recent10_avg = (account_info["rating"] / 100 - best30_avg * 0.75) / 0.25
                resp = {
                    "status": 0,
                    "content": {
                        "best30_avg": best30_avg,
                        "recent10_avg": recent10_avg,
                        "account_info": account_info,
                        "best30_list": score_info_list[:31],
                        "best30_overflow": score_info_list[31:41],
                        "best30_song_info": song_info_list[:31],
                        "best30_overflow_song_info": song_info_list[31:41],
                    },
                }
                return UserBest30(**resp)

    @classmethod
    async def get_user_best(cls, arcaea_id: str, songname: str, difficulty: int):
        url = f"{cls.base_url}/arcapi/user/best?user_name={arcaea_id}&song_name={songname}&difficulty={difficulty}&with_song_info=true"
        resp = await cls._quick_get(url=url)
        return UserBest(**resp.json())

    @classmethod
    async def get_song_random(cls, start: str, end: str):
        start = int(float(start.replace("+", ".5")) * 2)
        end = int(float(end.replace("+", ".5")) * 2)
        url = f"{cls.base_url}/arcapi/song/random?start={start}&end={end}&with_song_info=true"
        resp = await cls._quick_get(url=url)
        return SongRandom(**resp.json())

    @classmethod
    async def get_song_info(cls, songname: str):
        url = f"{cls.base_url}/arcapi/song/info?song_name={songname}"
        resp = await cls._quick_get(url=url)
        return AUASongInfo(**resp.json())

    @classmethod
    async def get_song_preview(cls, songname: str, difficulty: int):
        url = f"{cls.base_url}/arcapi/assets/preview?song_name={songname}&difficulty={difficulty}"
        resp = await cls._quick_get(url=url)
        if resp.status_code == 200:
            return resp.read()
        return "https://s2.loli.net/2022/06/18/Fo37uPwOtDzdlMb.jpg"
