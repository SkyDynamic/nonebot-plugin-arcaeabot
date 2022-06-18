from PIL import Image, ImageFont, ImageDraw
from typing import Tuple
from time import localtime, strftime

try:
    from numpy import average
except ImportError:

    def average(Itr):
        return sum(Itr) / len(Itr)


def open_img(image_path: str) -> Image.Image:
    with open(image_path, "rb") as f:
        image = Image.open(f).convert("RGBA")
    return image


def player_time_format(time_stamp: int) -> str:
    struct_time = localtime(time_stamp)
    return strftime("%Y-%m-%d %H:%M:%S", struct_time)


def get_average_color(image: Image.Image):
    pix = image.load()
    R_list = []
    G_list = []
    B_list = []
    width, height = image.size
    for x in range(int(width / 5)):
        for y in range(height):
            R_list.append(pix[x, y][0])
            G_list.append(pix[x, y][1])
            B_list.append(pix[x, y][2])
    R_average = int(average(R_list))
    G_average = int(average(G_list))
    B_average = int(average(B_list))
    return (R_average, G_average, B_average)


def is_dark(color: Tuple[int, int, int]):
    return (
        True if color[0] * 0.299 + color[1] * 0.587 + color[2] * 0.114 < 192 else False
    )


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


class DataText:
    def __init__(self, L, T, size, text, path, anchor="lt") -> None:
        self.L = L
        self.T = T
        self.text = str(text)
        self.path = path
        self.font = ImageFont.truetype(str(self.path), size)
        self.anchor = anchor


def write_text(
    image: Image.Image,
    font,
    text="text",
    pos=(0, 0),
    color=(255, 255, 255, 255),
    anchor="lt",
    stroke_width=0,
    stroke_fill="Black",
) -> Image.Image:
    rgba_image = image
    text_overlay = Image.new("RGBA", rgba_image.size, (255, 255, 255, 0))
    image_draw = ImageDraw.Draw(text_overlay)
    image_draw.text(
        pos,
        text,
        font=font,
        fill=color,
        anchor=anchor,
        stroke_width=stroke_width,
        stroke_fill=stroke_fill,
    )
    return Image.alpha_composite(rgba_image, text_overlay)


def draw_text(
    image,
    class_text: DataText,
    color: Tuple[int, int, int, int] = (255, 255, 255, 255),
    stroke_width=0,
    stroke_fill="Black",
) -> Image.Image:
    font = class_text.font
    text = class_text.text
    anchor = class_text.anchor
    color = color
    return write_text(
        image,
        font,
        text,
        (class_text.L, class_text.T),
        color,
        anchor,
        stroke_width=stroke_width,
        stroke_fill=stroke_fill,
    )
