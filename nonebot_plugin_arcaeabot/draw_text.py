from typing import Dict
from nonebot.adapters.onebot.v11 import MessageSegment
from io import BytesIO
from ._RHelper import RHelper
from PIL import Image

root = RHelper()


def open_img(image_path: str) -> Image.Image:
    with open(image_path, "rb") as f:
        image = Image.open(f).convert("RGBA")
    return image


def draw_song(song_info: Dict, difficulty: str = "all"):
    
    if difficulty == "all":
        image = open_img(root.assets.song / song_info["song_id"] / "base.jpg")
        result = "Name: " + song_info["difficulties"][0]["name_en"] + "\n"
        for i, value in enumerate(song_info["difficulties"]):
            _diff: float = value["rating"] / 10
            result += "[" + ["Past", "Persent", "Future", "Beyond"][i] + "]: " + str(_diff) + "\n"
    else:
        difficulty = int(difficulty)
        cover_name = "3.jpg" if difficulty == 3 else "base.jpg"
        image = open_img(root.assets.song / song_info["song_id"] / cover_name)
        song_info = song_info["difficulties"][difficulty]
        _diff: float = song_info["rating"] / 10
        _minite = str(int(song_info["time"]) / 60)
        _second = str(int(song_info["time"]) % 60)
        _name = song_info["name_jp"] + " [" + song_info["name_en"] + "]" if song_info["name_jp"] != "" else song_info["name_en"]
        result = "\n".join(
            [
                "Name: " + _name,
                "Artist: " + song_info["artist"],
                "bpm: " + str(song_info["bpm"]),
                "Package: " + song_info["set_friendly"],
                "Time: " + str(_minite) + ":" + str(_second),
                "Join_version: " + str(song_info["version"]),
                "Rating: " + str(_diff),
                "Note: " + str(song_info["note"]),
                "Chart_designer: " + song_info["chart_designer"],
                "Jacket_designer: " + song_info["jacket_designer"],
            ]
        )
        result += "\nIt need unlock by world mode" if song_info["world_unlock"] else ""

    buffer = BytesIO()
    image.save(buffer, "png")
    return MessageSegment.image(buffer) + "\n" + result
