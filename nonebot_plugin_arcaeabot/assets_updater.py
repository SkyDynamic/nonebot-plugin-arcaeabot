"""
 - Author: DiheChen
 - Date: 2021-08-15 22:01:10
 - LastEditTime: 2022-03-18 15:48:30
 - LastEditors: SEAFHMC
 - Description: None
 - GitHub: https://github.com/Chendihe4975
"""
from typing import List
from aiohttp import ClientSession
from os import path, listdir, makedirs
from nonebot import get_driver
from .config import Config
from nonebot.log import logger

plugin_config = Config.parse_obj(get_driver().config)
src_api_url = plugin_config.src_api_url
if src_api_url:
    logger.info("使用自定义src_api_url")
else:
    src_api_url = "http://107.182.17.60:17777/api/"

assets_path = path.abspath(path.join(path.dirname(__file__), "assets"))


async def check_song_update() -> List[str]:
    async with ClientSession() as session:
        async with session.get(src_api_url+"song_list", verify_ssl=False) as resp:
            result = list()
            for k, v in (await resp.json()).items():
                if k not in listdir(path.join(assets_path, "song")):
                    for link in v:
                        args = link.split("/")
                        makedirs(path.join(assets_path, "song", args[-2]), exist_ok=True)
                        async with session.get(link, verify_ssl=False) as res:
                            with open(path.join(assets_path, "song", args[-2], args[-1]), "wb") as file:
                                file.write(await res.read())
                                result.append(args[-2])
            return result


async def check_char_update() -> List[str]:
    async with ClientSession() as session:
        async with session.get(src_api_url+"char_list", verify_ssl=False) as resp:
            result = list()
            for k, v in (await resp.json()).items():
                if k not in listdir(path.join(assets_path, "char")):
                    async with session.get(v, verify_ssl=False) as res:
                        with open(path.join(assets_path, "char", k), "wb") as file:
                            file.write(await res.read())
                            result.append(k)
            return result
