from typing import List, Dict
from httpx import AsyncClient
from ..config import config
from nonebot.log import logger


async def get_user_info(arcaea_id: str, recent: bool = False) -> List[Dict]:
    async with AsyncClient() as client:
        # Config
        aua_ua = config.get_config("aua_ua")
        aua_url = config.get_config("aua_url")
        if aua_ua == "SECRET" or aua_url == "URL":
            logger.error("ArcaeaUnlimitedApi is not configured!")
        headers = {"User-Agent": aua_ua}
        # To str
        _recent = "&recent=1&withsonginfo=true" if recent is True else ""
        # request
        res = await client.get(
            url=f"{aua_url}/botarcapi/user/info?usercode={arcaea_id}{_recent}",
            headers=headers,
            timeout=100,
        )
        return res.json()


async def get_user_b30(
    arcaea_id: str, overflow: int = 0, recent: bool = False
) -> List[Dict]:
    async with AsyncClient() as client:
        # Config
        aua_ua = config.get_config("aua_ua")
        aua_url = config.get_config("aua_url")
        headers = {"User-Agent": aua_ua}
        # To str
        _overflow = "&overflow=" + str(overflow) if overflow > 0 else ""
        _recent = "&withrecent=true" if recent is False else ""
        # request
        res = await client.get(
            url=f"{aua_url}/botarcapi/user/best30?usercode={arcaea_id}{_overflow}{_recent}&withsonginfo=true",
            headers=headers,
            timeout=100,
        )
        return res.json()


async def get_user_recent(arcaea_id: str) -> List[Dict]:
    return await get_user_info(arcaea_id=arcaea_id, recent=True)


async def get_user_best(
    arcaea_id: str, song_id: str, difficulty: str, recent: bool = False
) -> List[Dict]:
    async with AsyncClient() as client:
        # Config
        aua_ua = config.get_config("aua_ua")
        aua_url = config.get_config("aua_url")
        headers = {"User-Agent": aua_ua}
        # to str
        _recent = "&withrecent=true" if recent is False else ""
        # request
        res = await client.get(
            url=f"{aua_url}/botarcapi/user/best?usercode={arcaea_id}&songid={song_id}&difficulty={difficulty}{_recent}&withsonginfo=true",
            headers=headers,
            timeout=100,
        )
        return res.json()
