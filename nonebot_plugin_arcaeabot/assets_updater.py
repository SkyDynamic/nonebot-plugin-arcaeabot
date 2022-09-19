from .resource_manager import assets_root
from .resource_manager import db_root as ROOT
from httpx import AsyncClient
from tqdm import tqdm
from os import listdir, makedirs, remove
from typing import List
from .config import config
from shutil import move, copy, rmtree
from zipfile import ZipFile
import ujson as json
from aiofiles import open as async_open
from re import match

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
}

src_api_url = config.get_config("src_url")


class AssetsUpdater:
    @staticmethod
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
                elif missed := (
                    {i.split("/")[-1] for i in v} - set(listdir(song_dir / k))
                ):
                    for link in v:
                        args = link.split("/")
                        if args[-1] in missed:
                            resp2 = await client.get(link)
                            with open(song_dir / args[-2] / args[-1], "wb") as file:
                                file.write(resp2.read())
                                result.append(args[-2])
            return result

    @staticmethod
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


class ApkUpdater:
    @classmethod
    async def download_apk(cls):
        async with AsyncClient(timeout=100, verify=False, headers=headers) as client:
            resp = await client.get(
                "https://webapi.lowiro.com/webapi/serve/static/bin/arcaea/apk"
            )
            with open(ROOT / "version.json", "w", encoding="UTF-8") as f:
                f.write(json.dumps(resp.json(), indent=2))
            download_link = resp.json()["value"]["url"]
            version = resp.json()["value"]["version"]
            async with async_open(ROOT / f"arcaea_{version}.apk", "wb") as f:
                async with client.stream("GET", download_link) as resp:
                    async for chunk in resp.aiter_bytes(1024 * 1024):
                        await f.write(chunk)

    @classmethod
    def unzip_apk(cls):
        rmtree(ROOT / "assets", ignore_errors=True)
        with open(ROOT / "version.json", "r", encoding="UTF-8") as f:
            version = json.loads(f.read())["value"]["version"]
        zip_file = ZipFile(ROOT / f"arcaea_{version}.apk")
        for file in zip_file.namelist():
            if match(r"^assets\/((char.*png)|(song.*(base|[0123]).jpg))$", file):
                zip_file.extract(file, ROOT)
        for song_id in listdir(ROOT / "assets" / "songs"):
            move(
                ROOT / "assets" / "songs" / song_id,
                ROOT / "assets" / "songs" / song_id.removeprefix("dl_"),
            )
        copy(ROOT / "assets" / "char" / "5.png", ROOT / "assets" / "char" / "5u.png")
        copy(
            ROOT / "assets" / "char" / "5_icon.png",
            ROOT / "assets" / "char" / "5u_icon.png",
        )
        zip_file.close()
        remove(ROOT / f"arcaea_{version}.apk")

    @classmethod
    async def update(cls):
        await cls.download_apk()
        cls.unzip_apk()

    @classmethod
    async def check_update(cls):
        with open(ROOT / "version.json", "r", encoding="UTF-8") as f:
            local_version = json.loads(f.read())["value"]["version"]
        async with AsyncClient(timeout=100, verify=False, headers=headers) as client:
            resp = await client.get(
                "https://webapi.lowiro.com/webapi/serve/static/bin/arcaea/apk"
            )
            online_version = resp.json()["value"]["version"]
        return local_version == online_version
