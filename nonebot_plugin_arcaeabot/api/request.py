from typing import Dict
from httpx import AsyncClient
from nonebot import get_driver
from nonebot.log import logger
from ..config import Config
from ..schema import UserInfo

plugin_config = Config.parse_obj(get_driver().config.dict())
if not plugin_config.aua_ua:
    logger.error("未在.env配置AUA_UA")
else:
    aua_ua = plugin_config.aua_ua
if not plugin_config.aua_url:
    logger.error("未在.env配置AUA_URL")
else:
    aua_url = plugin_config.aua_url


class API:
    headers = {"User-Agent": aua_ua}
    base_url = aua_url

    @classmethod
    async def quick_get(cls, url: str):
        async with AsyncClient(timeout=100) as client:
            resp = await client.get(url=url, headers=cls.headers)
        return resp

    @classmethod
    async def get_user_info(cls, arcaea_id: str):
        url = f"{cls.base_url}/botarcapi/user/info?user={arcaea_id}&recent=1&withsonginfo=true"
        resp = await cls.quick_get(url=url)
        return UserInfo(**resp.json())
