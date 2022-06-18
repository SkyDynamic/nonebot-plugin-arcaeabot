from .resource_manager import assets_root
from httpx import AsyncClient
from tqdm import tqdm
from os import listdir, makedirs
from typing import List
from .config import config

src_api_url = config.get_config("src_url")


async def check_song_update() -> List[str]:
    song_dir = assets_root / "song"
    song_dir.mkdir(exist_ok=True, parents=True)
    async with AsyncClient(timeout=100) as client:
        resp1 = await client.get(src_api_url + "song_list")
        result = []
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
    char_dir = assets_root / "char"
    char_dir.mkdir(exist_ok=True, parents=True)
    async with AsyncClient(timeout=100) as client:
        resp1 = await client.get(src_api_url + "char_list")
        result = list()
        for k, v in tqdm((resp1.json()).items()):
            if k not in listdir(char_dir):
                resp2 = await client.get(v)
                with open(char_dir / k, "wb") as file:
                    file.write(resp2.read())
                    result.append(k)
        return result
