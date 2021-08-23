"""
 - Author: DiheChen
 - Date: 2021-08-15 22:01:10
 - LastEditTime: 2021-08-18 02:47:18
 - LastEditors: DiheChen
 - Description: None
 - GitHub: https://github.com/Chendihe4975
"""
from typing import List
from aiohttp import ClientSession
from os import path, listdir, makedirs

assets_path = path.abspath(path.join(path.dirname(__file__), "assets"))


async def check_update() -> List[str]:
    async with ClientSession() as session:
        async with session.get("https://arcaea.dihe.moe/api/song_list", verify_ssl=False) as resp:
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