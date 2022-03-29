from nonebot import get_driver
from nonebot.log import logger
from ...config import Config
from typing import List, Dict
from httpx import AsyncClient
try:
    plugin_config = Config.parse_obj(get_driver().config)
    aua_url = plugin_config.aua_url
    aua_ua = plugin_config.aua_ua
except Exception as e:
    logger.error(e)
    logger.info("未监测到自定义aua配置!")
    aua_url = Config.aua_url
    aua_ua = Config.aua_ua
headers = {"User-Agent": aua_ua}

async def fetch_user_info(arcaea_id: str, recent_only: bool = False) -> List[Dict]:
    async with AsyncClient() as client:
        if recent_only:
            res = await client.get(
                url=f"{aua_url}/botarcapi/user/info?usercode={arcaea_id}&recent=1&withsonginfo=true",
                headers=headers,
                timeout=100)
            return res.json()
        else:
            res = await client.get(
                url=f"{aua_url}/botarcapi/user/best30?usercode={arcaea_id}&overflow=10&withrecent=true&withsonginfo=true",
                headers=headers,
                timeout=100)
            return res.json()
