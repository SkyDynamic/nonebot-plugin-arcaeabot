from typing import List
from httpx import AsyncClient
from os import path, listdir, makedirs
from tqdm import tqdm
from .config import config
from ._RHelper import RHelper

root = RHelper()


async def check_song_update() -> List[str]:
    async with AsyncClient() as client:

        src_api_url = config.get_config("src_url")
        song_dir = root.assets.song

        if not path.exists(song_dir):
            makedirs(song_dir, exist_ok=True)

        resp1 = await client.get(src_api_url + "song_list")
        result = list()
        for k, v in tqdm((resp1.json()).items()):
            if k not in listdir(song_dir):
                for link in v:
                    args = link.split("/")
                    makedirs(song_dir / args[-2], exist_ok=True)
                    resp2 = await client.get(link)
                    with open(song_dir / args[-2] / args[-1], "wb") as file:
                        file.write(resp2.read())
                        result.append(args[-2])
        return result


async def check_char_update() -> List[str]:
    async with AsyncClient() as client:

        src_api_url = config.get_config("src_url")
        char_dir = root.assets.char

        if not path.exists(char_dir):
            makedirs(char_dir, exist_ok=True)

        resp1 = await client.get(src_api_url + "char_list")
        result = list()
        for k, v in tqdm((resp1.json()).items()):
            if k not in listdir(char_dir):
                resp2 = await client.get(v)
                with open(char_dir / k, "wb") as file:
                    file.write(resp2.read())
                    result.append(k)
        return result
