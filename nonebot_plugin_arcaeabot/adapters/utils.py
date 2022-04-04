from os import path
from datetime import datetime
from time import localtime, mktime, strftime
from PIL import Image, ImageDraw, ImageFont
from ..assets import StaticPath, ASSETS
import ujson as json
from nonebot import get_driver
from ..config import Config
from typing import Optional


def player_time_format(time_stamp: int) -> str:
    struct_time = localtime(time_stamp / 1000)
    return strftime("%Y-%m-%d %H:%M:%S", struct_time)


def song_time_format(date):
    now = mktime(datetime.now().timetuple())
    return (now - date / 1000) / 86400


def choice_ptt_background(ptt: int):
    if ptt == -1:
        return "rating_off.png"
    ptt /= 100
    if ptt < 3:
        return "rating_0.png"
    elif 3 <= ptt < 7:
        return "rating_1.png"
    elif 7 <= ptt < 10:
        return "rating_2.png"
    elif 10 <= ptt < 11:
        return "rating_3.png"
    elif 11 <= ptt < 12:
        return "rating_4.png"
    elif 12 <= ptt < 12.5:
        return "rating_5.png"
    else:
        return "rating_6.png"


def track_complete(score: int, lost_count: int) -> str:
    if not lost_count:
        return path.join(ASSETS, "recent", "clear_pure.png") if score > int(1e7) else path.join(ASSETS, "recent", "clear_full.png")
    return path.join(ASSETS, "recent", "clear_normal.png")


class DataText:
    def __init__(self, L, T, size, text, path, anchor="lt") -> None:
        self.L = L
        self.T = T
        self.text = str(text)
        self.path = path
        self.font = ImageFont.truetype(self.path, size)
        self.anchor = anchor


def write_text(image: Image.Image, font, text="text", pos=(0, 0), color=(255, 255, 255, 255),
               anchor="lt", stroke_width=0, stroke_fill="Black") -> Image.Image:
    rgba_image = image
    text_overlay = Image.new("RGBA", rgba_image.size, (255, 255, 255, 0))
    image_draw = ImageDraw.Draw(text_overlay)
    image_draw.text(pos, text, font=font, fill=color, anchor=anchor, stroke_width=stroke_width, stroke_fill=stroke_fill)
    return Image.alpha_composite(rgba_image, text_overlay)


def draw_text(image, class_text: DataText, R=255, G=255, B=255, A=255, stroke_width=0, stroke_fill="Black") -> Image.Image:
    font = class_text.font
    text = class_text.text
    anchor = class_text.anchor
    color = (R, G, B, A)
    return write_text(image, font, text, (class_text.L, class_text.T), color, anchor, stroke_width=stroke_width, stroke_fill=stroke_fill)


def open_img(image_path: str) -> Image.Image:
    with open(image_path, "rb") as f:
        image = Image.open(f).convert("RGBA")
    return image


def get_song_info() -> list:
    with open(StaticPath.constants_json, "r", encoding="UTF-8") as f:
        return json.loads(f.read())


def adapter_selector() -> Optional[str]:
    plugin_config = Config.parse_obj(get_driver().config)
    api_in_use = plugin_config.api_in_use
    if api_in_use:
        pass
    else:
        api_in_use = "AUA"
    return api_in_use


api_in_use = adapter_selector().upper()
if api_in_use == "AUA":
    from ..adapters.aua.api import fetch_user_info
elif api_in_use == "ESTERTION":
    from ..adapters.estertion.api import fetch_user_info
else:
    pass
