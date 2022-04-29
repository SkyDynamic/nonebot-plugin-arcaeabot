from typing import Dict
from nonebot.adapters.onebot.v11 import MessageSegment
from io import BytesIO
from ._RHelper import RHelper
from PIL import Image
from time import localtime, strftime

root = RHelper()


def open_img(image_path: str) -> Image.Image:
    with open(image_path, "rb") as f:
        image = Image.open(f).convert("RGBA")
    return image


def time_format(time_stamp: int) -> str:
    struct_time = localtime(time_stamp)
    return strftime("%Y-%m-%d %H:%M:%S", struct_time)


def draw_help():
    return "\n".join(
            [
                "/arc bind <arcaea id> 进行绑定。",
                "/arc unbind 解除绑定。",
                "/arc info 查看绑定信息。",
                "/arc recent 查询上一次游玩记录。",
                "/arc b30 查询 best 30 记录。",
                "/arc assets_update 更新曲绘与立绘资源",
                "/arc best <曲名> [难度] 查询单曲最高分",
                "/arc song <曲名> [难度] 查询信息",
                "/arc random [难度] 随机指定难度的歌曲",
                "/arc random [难度min] [难度max] 随机指定难度区间的歌曲",
            ]
    )


def draw_song(song_info: Dict, difficulty: str = "all"):

    if difficulty == "all":
        image = open_img(root.assets.song / song_info["song_id"] / "base.jpg")
        result = "Name: " + song_info["difficulties"][0]["name_en"] + "\n"
        for i, value in enumerate(song_info["difficulties"]):
            _diff: float = value["rating"] / 10
            result += "[" + ["Past", "Present", "Future", "Beyond"][i] + "]: " + str(_diff) + "\n"
            result += "获取详细信息请在添加难度后缀" + "\n"
    else:
        difficulty = int(difficulty)
        cover_name = "3.jpg" if difficulty == 3 else "base.jpg"
        image = open_img(root.assets.song / song_info["song_id"] / cover_name)
        song_info = song_info["difficulties"][difficulty]
        _diff: float = song_info["rating"] / 10
        _minite = str(int(int(song_info["time"]) / 60))
        _second = str(int(song_info["time"]) % 60)
        _name = song_info["name_jp"] + " [" + song_info["name_en"] + "]" if song_info["name_jp"] != "" else song_info["name_en"]
        result = "\n".join(
            [
                "曲名: " + _name + " [" + ["Past", "Present", "Future", "Beyond"][difficulty] + "]",
                "曲师: " + song_info["artist"],
                "曲绘: " + song_info["jacket_designer"],
                "时长: " + str(_minite) + ":" + str(_second),
                "BPM: " + str(song_info["bpm"]),
                "谱师: " + song_info["chart_designer"],
                "Note数: " + str(song_info["note"]),
                "Rating: " + str(_diff),
                "隶属曲包: " + song_info["set_friendly"],
                "上线时间: " + time_format(int(song_info["date"]/10)*10)
            ]
        )
        result += "\n需要世界模式解锁" if song_info["world_unlock"] is True else ""
        result += "\n需要下载" if song_info["remote_download"] is True else ""

    buffer = BytesIO()
    image.save(buffer, "png")
    return MessageSegment.image(buffer) + "\n" + result
