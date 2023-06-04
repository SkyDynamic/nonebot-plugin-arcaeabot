from typing import Union
from ....schema import UserBest, UserInfo
from PIL import Image, ImageFilter
from ..utils import *
from ....resource_manager import StaticPath
from ....get_char_point import GetCharPoint


def draw_single_song(data: Union[UserBest, UserInfo], language: str):
    # User Info
    account_info = data.content.account_info
    name = account_info.name
    character = account_info.character
    is_char_uncapped_override = account_info.is_char_uncapped_override
    is_char_uncapped = account_info.is_char_uncapped
    if is_char_uncapped ^ is_char_uncapped_override:
        character = f"{character}u"
    else:
        character = character
    icon: str = f"{character}_icon.png"
    character_image: str = f"{character}.png"
    rating = account_info.rating
    # Score Info
    if isinstance(data, UserInfo):
        score_info = data.content.recent_score[0]
    else:
        score_info = data.content.record
    song_id = score_info.song_id
    song_info = data.content.song_info[0]
    health = score_info.health
    song_rating = score_info.rating
    shiny_perfect_count = score_info.shiny_perfect_count
    note = song_info.note
    # 判断用户的自定义语言
    if language == "en" or not language:
        song_name = song_info.name_en
    elif language == "jp":
        song_name = song_info.name_jp
    # 判断歌曲名是否拥有日文名，如没有则转为en
    if not song_name:
        song_name = song_info.name_en
    difficulty = score_info.difficulty
    score = score_info.score
    perfect_count = score_info.perfect_count
    near_count = score_info.near_count
    miss_count = score_info.miss_count
    # Back Ground
    cover_name = f"{difficulty}.jpg" if song_info.jacket_override else "base.jpg"
    image = Image.new("RGBA", (2388, 1668), (0, 0, 0, 0))
    song_cover = open_img(StaticPath.select_image("song", song_id, cover_name))
    image = image.filter(ImageFilter.GaussianBlur(radius=10))
    card = open_img(StaticPath.arcaea_0)
    image.alpha_composite(card)
    hp_base_bar = open_img(StaticPath.arcaea_style_dir / "hp_base.png")
    origin_size_w, origin_size_h = hp_base_bar.size
    hp_base_bar = hp_base_bar.resize((101, int(101 / origin_size_w * origin_size_h)))
    image.alpha_composite(hp_base_bar, (745, 662))
    image.alpha_composite(song_cover.resize((702, 702)), (56, 662))
    character_image_ = open_img(
        StaticPath.select_image("char", character_image)
    ).resize((1910, 1910))
    image.alpha_composite(character_image_, GetCharPoint(str(character)))
    score_card = open_img(StaticPath.arcaea_style_dir / "score.png")
    image.alpha_composite(score_card, (814, 659))
    top_bar = open_img(StaticPath.arcaea_style_dir / "top_bar.png")
    image.alpha_composite(top_bar, (0, 0))
    icon_border = open_img(StaticPath.arcaea_style_dir / "char_icon_border.png").resize(
        (199, 200)
    )
    image.alpha_composite(icon_border, (1084, -45))
    score_ = open_img(StaticPath.arcaea_style_dir / "score_.png")
    image.alpha_composite(score_, (1076, 1150))
    back_bottom = open_img(StaticPath.arcaea_style_dir / "back.png")
    origin_size_w, origin_size_h = back_bottom.size
    back_bottom = back_bottom.resize((405, int(405 / origin_size_w * origin_size_h)))
    image.alpha_composite(back_bottom, (0, 1549))
    share_bottom = open_img(StaticPath.arcaea_style_dir / "share.png")
    origin_size_w, origin_size_h = share_bottom.size
    share_bottom = share_bottom.resize((441, int(441 / origin_size_w * origin_size_h)))
    image.alpha_composite(share_bottom, (965, 1549))
    retry_bottom = open_img(StaticPath.arcaea_style_dir / "retry.png")
    origin_size_w, origin_size_h = retry_bottom.size
    retry_bottom = retry_bottom.resize((405, int(405 / origin_size_w * origin_size_h)))
    image.alpha_composite(retry_bottom, (1983, 1549))
    clear_type = ("TL", "NC", "FR", "PM", "EC", "HC")[score_info.clear_type]
    move_y = 0
    hp_top = open_img(StaticPath.arcaea_style_dir / "hp_top.png")
    origin_size_w, origin_size_h = hp_top.size
    hp_top = hp_top.resize((56, int(56 / origin_size_w * origin_size_h)))
    if clear_type != "HC" and clear_type != "EC":
        if health == 100:
            hp_bar = open_img(StaticPath.arcaea_style_dir / "hp_bar_clear.png").resize(
                (56, 702)
            )
            hp_bar.putalpha(100)
            image.alpha_composite(hp_bar, (758, 662))
        elif health >= 70:
            hp_bar = open_img(StaticPath.arcaea_style_dir / "hp_bar_clear.png").resize(
                (56, 702)
            )
            hp_size_x, hp_size_y = hp_bar.size
            move_y = int(hp_size_y * ((100 - health) / 100))
            hp_bar = hp_bar.crop((0, move_y, hp_size_x, hp_size_y))
            hp_bar.putalpha(100)
            image.alpha_composite(hp_bar, (758, 662 + move_y))
        elif 0 < health < 70:
            hp_bar = open_img(StaticPath.arcaea_style_dir / "hp_bar.png").resize(
                (56, 702)
            )
            hp_size_x, hp_size_y = hp_bar.size
            move_y = int(hp_size_y * ((100 - health) / 100))
            hp_bar = hp_bar.crop((0, move_y, hp_size_x, hp_size_y))
            hp_bar.putalpha(100)
            image.alpha_composite(hp_bar, (758, 662 + move_y))
        elif health == 0:
            move_y = int(702 * ((100 - health) / 100)) - 35
        image.alpha_composite(hp_top, (758, 662))
    elif clear_type == "HC":
        if health == 100:
            hp_bar = open_img(StaticPath.arcaea_style_dir / "hp_bar_hard.png").resize(
                (56, 702)
            )
            image.alpha_composite(hp_bar, (758, 662))
        elif 0 < health < 100:
            hp_bar = open_img(StaticPath.arcaea_style_dir / "hp_bar_hard.png").resize(
                (56, 702)
            )
            hp_size_x, hp_size_y = hp_bar.size
            move_y = int(hp_size_y * ((100 - health) / 100))
            hp_bar = hp_bar.crop((0, move_y, hp_size_x, hp_size_y))
            image.alpha_composite(hp_bar, (758, 662 + move_y))
        elif health == 0:
            move_y = int(702 * ((100 - health) / 100)) - 35
    elif clear_type == "EC":
        if health == 100:
            hp_bar = open_img(
                StaticPath.arcaea_style_dir / "hp_bar_easy_clear.png"
            ).resize((56, 702))
            hp_bar.putalpha(100)
            image.alpha_composite(hp_bar, (758, 662))
        elif health >= 70:
            hp_bar = open_img(
                StaticPath.arcaea_style_dir / "hp_bar_easy_clear.png"
            ).resize((56, 702))
            hp_size_x, hp_size_y = hp_bar.size
            move_y = int(hp_size_y * ((100 - health) / 100))
            hp_bar = hp_bar.crop((0, move_y, hp_size_x, hp_size_y))
            hp_bar.putalpha(100)
            image.alpha_composite(hp_bar, (758, 662 + move_y))
        elif 0 < health < 70:
            hp_bar = open_img(StaticPath.arcaea_style_dir / "hp_bar_easy.png").resize(
                (56, 702)
            )
            hp_size_x, hp_size_y = hp_bar.size
            move_y = int(hp_size_y * ((100 - health) / 100))
            hp_bar = hp_bar.crop((0, move_y, hp_size_x, hp_size_y))
            hp_bar.putalpha(100)
            image.alpha_composite(hp_bar, (758, 662 + move_y))
        elif health == 0:
            move_y = int(702 * ((100 - health) / 100)) - 35
        image.alpha_composite(hp_top, (758, 662))
    hp_grid = open_img(StaticPath.arcaea_style_dir / "hp_grid.png").resize((56, 702))
    image.alpha_composite(hp_grid, (758, 662))
    write_health = DataText(787, 683 + move_y, 28, health, StaticPath.exo_regular, "mm")
    image = draw_text(image, write_health, stroke_fill="Black", stroke_width=2)
    # Draw User Info
    icon = open_img(StaticPath.select_image("char", icon))
    image.alpha_composite(icon, (1100, -30))
    ptt = open_img(StaticPath.ptt_dir / choice_ptt_background(rating)).resize(
        (119, 119)
    )
    image.alpha_composite(ptt, (1190, 55))
    if rating == -1:
        write_ptt = DataText(1250, 125, 40, "--", StaticPath.exo_semibold, anchor="mb")
        image = draw_text(image, write_ptt, stroke_fill="Black", stroke_width=2)
    else:
        raw_ptt = f"{(rating/100):.2f}".split(".")
        write_ptt_head = DataText(
            1240, 128, 40, raw_ptt[0], StaticPath.exo_semibold, anchor="rs"
        )
        image = draw_text(image, write_ptt_head, stroke_fill="Black", stroke_width=2)
        write_ptt_tail = DataText(
            1240, 128, 35, "." + raw_ptt[1], StaticPath.exo_semibold, anchor="ls"
        )
        image = draw_text(image, write_ptt_tail, stroke_fill="Black", stroke_width=2)
    write_user_name = DataText(1085, 50, 65, name, StaticPath.exo_medium, anchor="rm")
    image = draw_text(image, write_user_name, (91, 79, 83))
    # Draw Score Info
    write_play_ptt = DataText(58, 580, 50, "Play Ptt:", StaticPath.exo_regular, "lm")
    image = draw_text(image, write_play_ptt, (111, 111, 111))
    write_song_rating = DataText(
        255, 582, 50, str(round(song_rating, 4)), StaticPath.exo_regular, "lm"
    )
    image = draw_text(image, write_song_rating, (111, 111, 111))
    write_song_name_shodow = DataText(
        1209, 349, 108, song_name, StaticPath.nsc_regular, "mm"
    )
    write_song_name = DataText(1205, 345, 108, song_name, StaticPath.nsc_regular, "mm")
    image = draw_text(image, write_song_name_shodow, "black")
    image = draw_text(image, write_song_name, "white")
    write_author = DataText(
        1205, 445, 52, song_info.artist, StaticPath.nsc_regular, "mm"
    )
    write_author_shadow = DataText(
        1209, 449, 52, song_info.artist, StaticPath.nsc_regular, "mm"
    )
    image = draw_text(image, write_author_shadow, "black")
    image = draw_text(image, write_author, "white")
    song_level = str(song_info.rating / 10).split(".")
    song_level_format = song_level[0]
    if int(song_level[1]) >= 7 and int(song_level[0]) >= 9:
        song_level_format = f"{song_level[0]}+"
    write_difficulty = DataText(
        58,
        630,
        48,
        ["Past", "Present", "Future", "Beyond"][difficulty] + " " + song_level_format,
        StaticPath.kazesawa_regular,
        "lm",
    )
    diff_color = ((20, 165, 215), (120, 150, 80), (115, 35, 100), (166, 20, 49))[
        difficulty
    ]
    image = draw_text(image, write_difficulty, diff_color)
    track_type = get_track_type(clear_type)
    track_info = open_img(StaticPath.is_failed(track_type))
    origin_size_w, origin_size_h = track_info.size
    track_info = track_info.resize((996, int(996 / origin_size_w * origin_size_h)))
    image.alpha_composite(track_info, (700, 515))
    write_score = DataText(
        1205,
        740,
        108,
        format(score, ",").replace(",", "'").rjust(10, "0"),
        StaticPath.andrea,
        "mm",
    )
    write_score_shadow = DataText(
        1209,
        744,
        108,
        format(score, ",").replace(",", "'").rjust(10, "0"),
        StaticPath.andrea,
        "mm",
    )
    if shiny_perfect_count == note:
        image = draw_text(image, write_score_shadow, (0, 160, 170, 120))
    else:
        image = draw_text(image, write_score_shadow, "black")
    image = draw_text(image, write_score, "white")
    grade_resource = get_grade(score)
    grade = open_img(grade_resource)
    origin_size_w, origin_size_h = grade.size
    grade = grade.resize((325, int(325 / origin_size_w * origin_size_h)))
    image.alpha_composite(grade, (1035, 905))
    write_pure = DataText(1210, 1135, 64, perfect_count, StaticPath.andrea)
    image = draw_text(image, write_pure, (111, 111, 111), 8, "white")
    write_shiny_pure = DataText(
        1365, 1143, 40, f"+{shiny_perfect_count}", StaticPath.andrea, "lt"
    )
    image = draw_text(image, write_shiny_pure, (111, 111, 111), 2, "white")
    write_far = DataText(1210, 1205, 64, near_count, StaticPath.andrea)
    image = draw_text(image, write_far, (111, 111, 111), 8, "white")
    write_lost = DataText(1210, 1275, 64, miss_count, StaticPath.andrea)
    image = draw_text(image, write_lost, (111, 111, 111), 8, "white")
    write_PLAYTIME = DataText(945, 1345, 48, "Play Time:", StaticPath.exo_regular)
    image = draw_text(image, write_PLAYTIME, (110, 110, 110), 2, "white")
    write_playtime = DataText(
        1175,
        1350,
        45,
        player_time_format(score_info.time_played.timestamp()),
        StaticPath.exo_regular,
    )
    image = draw_text(image, write_playtime, (110, 110, 110), 2, "white")
    return image


def get_grade(score: int) -> StaticPath:
    if score >= 9900000:
        return StaticPath.grade_ex_plus
    elif 9900000 > score >= 9800000:
        return StaticPath.grade_ex
    elif 9800000 > score >= 9500000:
        return StaticPath.grade_aa
    elif 9500000 > score >= 9200000:
        return StaticPath.grade_a
    elif 9200000 > score >= 8900000:
        return StaticPath.grade_b
    elif 8900000 > score >= 8600000:
        return StaticPath.grade_c
    elif score < 8600000:
        return StaticPath.grade_d


def get_track_type(type: str):
    if type in ["NC", "EC", "HC"]:
        return "clear_normal"
    elif type == "PM":
        return "clear_pure"
    elif type == "FR":
        return "clear_full"
    elif type == "TL":
        return "clear_fail"
