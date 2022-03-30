from nonebot import get_driver
from nonebot.log import logger
from ...config import Config
from typing import List, Dict
from httpx import AsyncClient
from ..utils import adapter_selector

if adapter_selector().upper() == "AUA":
    plugin_config = Config.parse_obj(get_driver().config)
    aua_url = plugin_config.aua_url
    aua_ua = plugin_config.aua_ua
    if aua_url:
        logger.info("使用自定义aua_url")
    else:
        aua_url = "SECRET"
        logger.error("若选用aua, 请配置aua_url")
    if aua_ua:
        logger.info("使用自定义aua_ua")
    else:
        aua_ua = "SECRET"
        logger.error("若选用aua, 请配置aua_ua")

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
