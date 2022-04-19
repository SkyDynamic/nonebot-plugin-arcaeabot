from PIL import Image
from typing import Tuple, Dict
from .assets import StaticPath
from .utils import text_image, open_img, get_song_info, get_average_color, is_dark, player_time_format, DataText, draw_text, choice_ptt_background


def draw_score_bg(
    average_color: Tuple[int, int, int], song_cover: Image.Image, mask: Image.Image
) -> Image.Image:
    invisible_bg = Image.new("RGBA", (560, 270), (0, 0, 0, 0))
    score_bg = Image.new("RGBA", (560, 270))
    score_bg.alpha_composite(song_cover, (290, 0))
    left = Image.new("RGBA", (290, 270), average_color)
    score_bg.alpha_composite(left)
    for i in range(230):
        score_bg.alpha_composite(
            Image.new(
                "RGBA",
                (1, 270),
                (
                    average_color[0],
                    average_color[1],
                    average_color[2],
                    255 - int(1.2 * i),
                ),
            ),
            (290+ i, 0),
        )
    out = Image.composite(score_bg, invisible_bg, mask)
    return out

def draw_score_detail(data: Dict, rank: int, song_id: str, mask: Image.Image) -> Image.Image:
    # Frame
    song_info = get_song_info(song_id)
    diff = data["difficulty"]
    cover_name = "3.jpg" if diff ==3 else "base.jpg"
    song_background = open_img(StaticPath.song_dir/data["song_id"]/cover_name).resize((270, 270))
    average_color = get_average_color(song_background)
    contrast_degree = 7 if is_dark(average_color) else 0.3
    image = draw_score_bg(average_color, song_background, mask)
    diff_background = open_img(StaticPath.diff_dir/["PST.png", "PRS.png", "FTR.png", "BYD.png"][diff]).resize((14, 48))
    image.alpha_composite(diff_background, (24, 24))
    song_name = song_info["title_localized"]["en"]
    song_name = song_name if len(song_name)<19 else song_name[:18]+"…"
    write_song_name = text_image(song_name, StaticPath.kazesawa_regular, 40, average_color, contrast_degree)
    image.alpha_composite(write_song_name, (45, 32))
    write_score = text_image(f'{data["score"]:,}', StaticPath.exo_medium, 40, average_color, contrast_degree)
    image.alpha_composite(write_score, (45, 80))
    write_ranking = text_image(f'#{rank + 1}', StaticPath.exo_medium, 30, "white",stroke_fill="black", stroke_width=1)
    image.alpha_composite(write_ranking, (490, 20))
    # Table
    table = open_img(StaticPath.table)
    image.alpha_composite(table)
    write_P = text_image("P", StaticPath.andrea, 35, average_color, contrast_degree, stroke_fill=average_color, stroke_width=1)
    image.alpha_composite(write_P, (50, 130))
    write_F = text_image("F", StaticPath.andrea, 35, average_color, contrast_degree, stroke_fill=average_color, stroke_width=1)
    image.alpha_composite(write_F, (50, 175))
    write_L = text_image("L", StaticPath.andrea, 35, average_color, contrast_degree, stroke_fill=average_color, stroke_width=1)
    image.alpha_composite(write_L, (50, 220))
    write_PTT = text_image("PTT", StaticPath.exo_medium, 25, average_color, contrast_degree)
    image.alpha_composite(write_PTT, (250, 130))
    write_DATE = text_image("DATE", StaticPath.exo_medium, 25, average_color, contrast_degree)
    image.alpha_composite(write_DATE, (250, 200))
    write_arrow = text_image(">", StaticPath.andrea, 50, average_color, contrast_degree)
    image.alpha_composite(write_arrow, (300, 150))
    # Count
    write_p_count = text_image(str(data["perfect_count"]), StaticPath.kazesawa_regular, 30, average_color, contrast_degree)
    image.alpha_composite(write_p_count, (75, 130))
    write_sp_count = text_image(f'+{data["shiny_perfect_count"]}', StaticPath.kazesawa_regular, 20, average_color, contrast_degree)
    image.alpha_composite(write_sp_count, (155, 130))
    write_near_count = text_image(str(data["near_count"]), StaticPath.kazesawa_regular, 30, average_color, contrast_degree)
    image.alpha_composite(write_near_count, (75, 175))
    write_miss_count = text_image(str(data["miss_count"]), StaticPath.kazesawa_regular, 30, average_color, contrast_degree)
    image.alpha_composite(write_miss_count, (75, 220))
    write_time = text_image(player_time_format(data["time_played"]), StaticPath.kazesawa_regular, 25, average_color, contrast_degree)
    image.alpha_composite(write_time, (250, 230))
    write_constant = text_image(f'{song_info["difficulties"][data["difficulty"]]["rating"]:.1f}',  StaticPath.kazesawa_regular, 25, average_color, contrast_degree)
    image.alpha_composite(write_constant, (250, 165))
    write_rating = text_image(f'{data["rating"]:.3f}', StaticPath.kazesawa_regular, 25, average_color, contrast_degree)
    image.alpha_composite(write_rating, (320, 148))
    return image


def draw_b30(data):
    B30_bg = open_img(StaticPath.B30_bg)
    #User Info
    name: str = data.name
    rating: str = data.rating
    best: float = data.best
    recent: float = data.recent
    icon: str = data.icon
    icon = open_img(StaticPath.char_dir/icon).resize((250, 250))
    B30_bg.alpha_composite(icon, (75, 130))
    ptt_background = open_img(StaticPath.ptt_dir/choice_ptt_background(rating)).resize((150, 150))
    B30_bg.alpha_composite(ptt_background, (200, 280))
    raw_ptt = str(round(rating/100, 2)).split(".")
    write_ptt_head = DataText(270, 370, 50, raw_ptt[0], StaticPath.exo_medium, anchor="rs")
    B30_bg = draw_text(B30_bg, write_ptt_head, stroke_fill="Black", stroke_width=2)
    write_ptt_tail = DataText(270, 370, 40, "."+raw_ptt[1], StaticPath.exo_medium, anchor="ls")
    B30_bg = draw_text(B30_bg, write_ptt_tail, stroke_fill="Black", stroke_width=2)
    write_arcname = DataText(355, 280, 100, name,
                                StaticPath.exo_medium, anchor="lb")
    B30_bg = draw_text(B30_bg, write_arcname)
    arcaea_id = "114514009"
    write_arcaea_id = DataText(
        380, 360, 60, f"ID:{arcaea_id}", StaticPath.exo_medium, anchor="lb")
    B30_bg = draw_text(B30_bg, write_arcaea_id)
    write_r10 = DataText(
        1000, 560, 100, f"Recent 10: {recent:.3f}", StaticPath.exo_medium, anchor="lb")
    B30_bg = draw_text(B30_bg, write_r10)
    write_b30 = DataText(
        200, 560, 100, f"Best 30: {best:.3f}", StaticPath.exo_medium, anchor="lb")
    B30_bg = draw_text(B30_bg, write_b30)
    #Score Info
    score_info_list = data.score_info_list
    divider = open_img(StaticPath.divider).resize((2000, 50))
    background_y = 640
    background_x = 0
    mask = Image.open(StaticPath.mask)
    if True:
        for num, data in enumerate(score_info_list):
            if num == 39:
                break
            if num % 3 == 0:
                background_y += 300 if num != 0 else 0
                background_x = 100
            else:
                background_x += 620
            if num / 3==10:
                background_y += 100
                B30_bg.alpha_composite(divider, (0, background_y-87))
            B30_bg.alpha_composite(draw_score_detail(data, rank=num, song_id=data["song_id"], mask=mask), (background_x, background_y))
    return B30_bg