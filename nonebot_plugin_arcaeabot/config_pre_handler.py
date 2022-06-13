from nonebot import get_driver
from nonebot.log import logger
from .config import Config as PluginConfig


class Config:
    plugin_config = PluginConfig.parse_obj(get_driver().config.dict())
    if not plugin_config.aua_ua:
        logger.error("未在.env配置AUA_UA")
    else:
        aua_ua = plugin_config.aua_ua
    if not plugin_config.aua_url:
        logger.error("未在.env配置AUA_URL")
    else:
        aua_url = plugin_config.aua_url
    if not plugin_config.src_api_url:
        src_api_url = "https://api.ritsuki.top/api/"
    else:
        src_api_url = plugin_config.src_api_url
