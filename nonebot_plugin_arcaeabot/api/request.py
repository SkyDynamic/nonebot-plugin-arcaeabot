from typing import Union
from httpx import AsyncClient
from ..config import config
from ..schema import UserInfo, UserBest30, UserBest, SongRandom, AUASongInfo

aua_ua = config.get_config("aua_ua")
aua_url = config.get_config("aua_url")


class API:
    headers = {"User-Agent": aua_ua}
    base_url = aua_url

    @classmethod
    async def _quick_get(cls, url: str):
        async with AsyncClient(timeout=100) as client:
            resp = await client.get(url=url, headers=cls.headers)
        return resp

    @classmethod
    async def get_user_info(cls, arcaea_id: str):
        url = f"{cls.base_url}/botarcapi/user/info?user={arcaea_id}&recent=1&withsonginfo=true"
        resp = await cls._quick_get(url=url)
        return UserInfo(**resp.json())

    @classmethod
    async def get_user_b30(cls, arcaea_id: str):
        url = f"{cls.base_url}/botarcapi/user/best30?usercode={arcaea_id}&withrecent=false&overflow=10&withsonginfo=true"
        resp = await cls._quick_get(url=url)
        return UserBest30(**resp.json())

    @classmethod
    async def get_user_best(cls, arcaea_id: str, songname: str, difficulty: int):
        url = f"{cls.base_url}/botarcapi/user/best?user={arcaea_id}&songname={songname}&difficulty={difficulty}&withsonginfo=true"
        resp = await cls._quick_get(url=url)
        return UserBest(**resp.json())

    @classmethod
    async def get_song_random(cls, start: Union[str, float], end: Union[str, float]):
        url = f"{cls.base_url}/botarcapi/song/random?start={start}&end={end}&withsonginfo=true"
        resp = await cls._quick_get(url=url)
        return SongRandom(**resp.json())

    @classmethod
    async def get_song_info(cls, songname: str):
        url = f"{cls.base_url}/botarcapi/song/info?songname={songname}"
        resp = await cls._quick_get(url=url)
        return AUASongInfo(**resp.json())

    @classmethod
    async def get_song_preview(cls, songname: str, difficulty: int):
        url = f"{cls.base_url}/botarcapi/assets/preview?songname={songname}&difficulty={difficulty}"
        resp = await cls._quick_get(url=url)
        if resp.status_code == 200:
            return resp.read()
        return "https://s2.loli.net/2022/06/18/Fo37uPwOtDzdlMb.jpg"
