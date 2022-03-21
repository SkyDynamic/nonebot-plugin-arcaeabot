"""
 - Author: DiheChen
 - Date: 2021-08-15 22:01:10
 - LastEditTime: 2021-08-19 21:40:04
 - LastEditors: DiheChen
 - Description: None
 - GitHub: https://github.com/Chendihe4975
"""
from os import path
from datetime import datetime
from time import localtime, mktime, strftime

from PIL import Image, ImageDraw, ImageFont
from nonebot.adapters.onebot.v11 import MessageSegment

from .assets import StaticPath, ASSETS
from .request import fetch_user_info
import ujson as json


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


def write_text(image: Image.Image, font, text="text", pos=(0, 0), color=(255, 255, 255, 255), anchor="lt", stroke_width=0, stroke_fill="Black") -> Image.Image:
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


class UserArcaeaInfo:
    querying = list()

    @staticmethod
    def is_querying(arcaea_id: int) -> bool:
        return arcaea_id in UserArcaeaInfo.querying

    @staticmethod
    async def draw_best30_image(arcaea_id: int):
        UserArcaeaInfo.querying.append(arcaea_id)
        try:
            data = await fetch_user_info(arcaea_id, recent_only=False)
        except Exception as e:
            UserArcaeaInfo.querying.remove(arcaea_id)
            return str(e)
        UserArcaeaInfo.querying.remove(arcaea_id)
        name: str = data[2]["data"]["name"]
        character: int = data[2]["data"]["character"]
        is_char_uncapped: bool = data[2]["data"]["is_char_uncapped"]
        is_char_uncapped_override: bool = data[2]["data"]["is_char_uncapped_override"]
        rating: str = data[2]["data"]["rating"]
        score_info_list: list = data[3:]
        score_info_list.sort(
            key=lambda v: v["data"][0]["rating"], reverse=True)
        best_total: float = .0
        for i in (range(30) if len(score_info_list) >= 30 else range(len(score_info_list))):
            best_total += score_info_list[i]["data"][0]["rating"]
        best: float = best_total / 30
        recent: float = (rating / 100 - best * 0.75) / 0.25
        icon: str = f"{character}u_icon.png" if is_char_uncapped ^ is_char_uncapped_override else f"{character}_icon.png"
        image = Image.new("RGBA", (1800, 3000))
        background = open_img(StaticPath.b30_background)
        image.alpha_composite(background)
        icon = open_img(StaticPath.select_image(
            "char", icon)).resize((250, 250))
        image.alpha_composite(icon, (175, 275))
        ptt_background = open_img(
            StaticPath.select_image("ptt", choice_ptt_background(rating))).resize((150, 150))
        image.alpha_composite(ptt_background, (300, 400))
        write_ptt = DataText(375, 475, 45, rating / 100 if rating != -
                             1 else "--", StaticPath.exo_regular, anchor="mm")
        image = draw_text(image, write_ptt, stroke_fill="Black", stroke_width=2)
        write_arcname = DataText(455, 400, 85, name,
                                 StaticPath.geosans_light, anchor="lb")
        image = draw_text(image, write_arcname)
        write_arcaea_id = DataText(
            480, 475, 60, f"ID:{arcaea_id}", StaticPath.exo_regular, anchor="lb")
        image = draw_text(image, write_arcaea_id)
        write_r10 = DataText(
            1100, 400, 60, f"Recent 10: {recent:.3f}", StaticPath.exo_regular, anchor="lb")
        image = draw_text(image, write_r10)
        w_b30 = DataText(
            1100, 425, 60, f"Best 30: {best:.3f}", StaticPath.exo_regular)
        image = draw_text(image, w_b30)
        background_y = 580
        background_x = 0
        for num, i in enumerate(score_info_list):
            if num == 30:
                break
            if num % 3 == 0:
                background_y += 240 if num != 0 else 0
                background_x = 30
            else:
                background_x += 600
            data = i["data"][0]
            best30_background = open_img(
                StaticPath.b30_score_background)
            image.alpha_composite(
                best30_background, (10 + background_x, background_y))
            song_background = open_img(
                StaticPath.select_image("song", data["song_id"], "base.jpg")).resize((190, 190))
            image.alpha_composite(
                song_background, (35 + background_x, 5 + background_y))
            diff_background = open_img(
                StaticPath.select_image("diff", ["PST.png", "PRS.png", "FTR.png", "BYD.png"][data["difficulty"]])).resize((72, 72))
            image.alpha_composite(
                diff_background, (161 + background_x, background_y - 3))
            rank_background = open_img(StaticPath.check_rank_background(
                score=data["score"], failed=(data["health"] == -1))).resize((135, 65))
            image.alpha_composite(
                rank_background, (395 + background_x, 95 + background_y))
            write_constant = DataText(223 + background_x, 12 + background_y, 20,
                                      f'{data["constant"]:.1f}', StaticPath.exo_regular, anchor='rt')
            image = draw_text(image, write_constant)
            write_ranking = DataText(480 + background_x, background_y, 45,
                                     f'#{num + 1}', StaticPath.exo_regular, anchor='lm')
            image = draw_text(image, write_ranking)
            write_score = DataText(235 + background_x, 15 + background_y,
                                   55, f'{data["score"]:,}', StaticPath.geosans_light)
            image = draw_text(image, write_score)
            write_PURE = DataText(235 + background_x, 75 + background_y,
                                  30, 'PURE', StaticPath.geosans_light)
            image = draw_text(image, write_PURE)
            write_p_count = DataText(335 + background_x, 75 + background_y,
                                     30, data["perfect_count"], StaticPath.geosans_light)
            image = draw_text(image, write_p_count)
            write_sp_count = DataText(400 + background_x, 75 + background_y,
                                      20, f'+{data["shiny_perfect_count"]}', StaticPath.geosans_light)
            image = draw_text(image, write_sp_count)
            write_far_text = DataText(
                235 + background_x, 105 + background_y, 30, 'FAR', StaticPath.geosans_light)
            image = draw_text(image, write_far_text)
            write_far_count = DataText(335 + background_x, 105 + background_y,
                                       30, data["near_count"], StaticPath.geosans_light)
            image = draw_text(image, write_far_count)
            write_lost_text = DataText(
                235 + background_x, 135 + background_y, 30, 'LOST', StaticPath.geosans_light)
            image = draw_text(image, write_lost_text)
            write_lost_count = DataText(
                335 + background_x, 135 + background_y, 30, data["miss_count"], StaticPath.geosans_light)
            image = draw_text(image, write_lost_count)
            write_rating_text = DataText(
                235 + background_x, 170 + background_y, 30, 'Rating:', StaticPath.geosans_light)
            image = draw_text(image, write_rating_text)
            write_rating = DataText(335 + background_x, 170 + background_y,
                                    30, f'{data["rating"]:.3f}', StaticPath.geosans_light)
            image = draw_text(image, write_rating)
            write_time = DataText(280 + background_x, 210 + background_y, 30,
                                  player_time_format(data["time_played"]), StaticPath.exo_regular, anchor='mm')
            image = draw_text(image, write_time)
            if song_time_format(data["time_played"]) <= 7:
                new_background = open_img(StaticPath.new_background)
                image.alpha_composite(
                    new_background, (background_x - 23, background_y))
        image.save(StaticPath.output(str(arcaea_id)))
        return MessageSegment.image("file:///"+StaticPath.output(str(arcaea_id)))

    @staticmethod
    async def draw_recent_image(arcaea_id: int):
        UserArcaeaInfo.querying.append(arcaea_id)
        try:
            data = (await fetch_user_info(arcaea_id, recent_only=True))[0]["data"]
        except Exception as e:
            UserArcaeaInfo.querying.remove(arcaea_id)
            return str(e)
        UserArcaeaInfo.querying.remove(arcaea_id)
        name: str = data["name"]
        character: int = data["character"]
        is_char_uncapped: bool = data["is_char_uncapped"]
        is_char_uncapped_override: bool = data["is_char_uncapped_override"]
        icon = f"{character}u_icon.png" if is_char_uncapped ^ is_char_uncapped_override else f"{character}_icon.png"
        rating: int = data["rating"]
        song_id: str = data["recent_score"][0]["song_id"]
        song_info: list = get_song_info()
        song_name: str = song_info[0]["data"][song_id]["en"]
        author_name: str = song_info[1]["data"][song_id]
        difficulty: int = data["recent_score"][0]["difficulty"]
        score: int = data["recent_score"][0]["score"]
        shiny_perfect_count: int = data["recent_score"][0]["shiny_perfect_count"]
        perfect_count: int = data["recent_score"][0]["perfect_count"]
        near_count: int = data["recent_score"][0]["near_count"]
        miss_count: int = data["recent_score"][0]["miss_count"]
        health: int = data["recent_score"][0]["health"]
        song_rating: float = data["recent_score"][0]["rating"]
        constant: float = data["recent_score"][0]["constant"]
        image = Image.new("RGBA", (1280, 720))
        background = open_img(StaticPath.recent_background)
        image.alpha_composite(background)
        icon = open_img(StaticPath.select_image(
            "char", icon)).resize((130, 130))
        image.alpha_composite(icon, (575, -15))
        full_character = f"{character}u.png" if is_char_uncapped ^ is_char_uncapped_override else f"{character}.png"
        song_cover = open_img(StaticPath.select_image(
            "song", data["recent_score"][0]["song_id"], "base.jpg")).resize((375, 375))
        image.alpha_composite(song_cover, (40, 290))
        track_info = open_img(StaticPath.is_failed(
            character=character, health=health, score=score, lost_count=miss_count))
        origin_size_w, origin_size_h = track_info.size
        track_info = track_info.resize((545, int(545/origin_size_w*origin_size_h)))
        image.alpha_composite(track_info, (365, 215))
        character = open_img(StaticPath.select_image("char", full_character
                                                     )).resize((1000, 1000))
        image.alpha_composite(character, (650, 125))
        res_scoresection_high = open_img(
            StaticPath.res_scoresection_high)
        image.alpha_composite(res_scoresection_high, (441, 290))
        hp_bar_base = open_img(StaticPath.hp_base if difficulty !=
                               3 else StaticPath.hp_beyond_marker).resize((45, 397))
        image.alpha_composite(hp_bar_base, (410, 290))
        hb_bar = open_img(StaticPath.select_hp_bar_image(
            character)).resize((27, 375))
        hb_bar = hb_bar.crop((0, 0, 27, int(health/100 * 375)))
        image.alpha_composite(hb_bar, (415, int(665 - health/100 * 375)))
        hp_grid = open_img(StaticPath.hp_grid).resize((27, 375))
        image.alpha_composite(hp_grid, (415, 290))
        rating_image = open_img(StaticPath.select_rating_image(
            score=score, failed=(health == -1)))
        image.alpha_composite(rating_image, (595, 417))
        ptt = open_img(StaticPath.select_image("ptt",
                                               choice_ptt_background(rating))).resize((75, 75))
        image.alpha_composite(ptt, (655, 50))
        write_player_name = DataText(
            (560 - len(name)*20), 20, 40, name, StaticPath.exo_regular)
        image = draw_text(image, write_player_name, 96, 75, 84, 255)
        write_arcaea_id = DataText(
            920, 20, 40, f"id: {arcaea_id}", StaticPath.exo_regular)
        image = draw_text(image, write_arcaea_id, 96, 75, 84, 255)
        write_song_name = DataText(
            (640 - len(song_name) / 2 * 20), 115, 40,
            song_name.capitalize(), StaticPath.NotoSansCJKsc_Regular)
        image = draw_text(image, write_song_name)
        write_author = DataText(
            (640 - len(author_name) / 2 * 12), 165, 24,
            author_name.capitalize(), StaticPath.NotoSansCJKsc_Regular)
        image = draw_text(image, write_author)
        write_score = DataText((640-len(str(score))/2 * 30), 310,
                               55, format(score, ",").replace(",", "'"), StaticPath.geosans_light)
        image = draw_text(image, write_score)
        write_difficulty = DataText(40, 230, 40, [
                                    "Past", "Persent", "Future", "Beyond"][difficulty]+" " + str(int(constant)), StaticPath.geosans_light)
        image = draw_text(image, write_difficulty, 96, 75, 84, 255)
        write_recent_text = DataText(
            40, 20, 45, "Recent", StaticPath.exo_regular)
        image = draw_text(image, write_recent_text, 96, 75, 84, 255)
        pure = open_img(StaticPath.pure).resize((90, 90))
        image.alpha_composite(pure, (550, 500))
        far = open_img(StaticPath.far).resize((90, 90))
        image.alpha_composite(far, (550, 540))
        lost = open_img(StaticPath.lost).resize((90, 90))
        image.alpha_composite(lost, (550, 580))
        write_song_rating = DataText(660, 380, 25, str(
            round(song_rating, 2)), StaticPath.geosans_light)
        image = draw_text(image, write_song_rating)
        write_perfect_count = DataText(670+(4-len(str(perfect_count))/2 * 15), 530, 30, str(
            perfect_count), StaticPath.geosans_light)
        image = draw_text(image, write_perfect_count, 137, 137, 137, 255)
        write_shiny_perfect_count = DataText(720, 530, 30, "+ "+str(
            shiny_perfect_count), StaticPath.geosans_light)
        image = draw_text(image, write_shiny_perfect_count, 137, 137, 137, 255)
        write_near_count = DataText(670+(4-len(str(near_count))/2 * 15), 575, 30, str(
            near_count), StaticPath.geosans_light)
        image = draw_text(image, write_near_count, 137, 137, 137, 255)
        write_miss_count = DataText(670+(4-len(str(miss_count))/2 * 15), 610, 30, str(
            miss_count), StaticPath.geosans_light)
        image = draw_text(image, write_miss_count, 137, 137, 137, 255)
        write_ptt = DataText(660, 70, 30, str(
            round(rating/100, 2)), StaticPath.exo_regular)
        image = draw_text(image, write_ptt, stroke_fill="Black", stroke_width=2)
        image.save(StaticPath.output(str(arcaea_id) + "_recent"))
        return MessageSegment.image("file:///"+StaticPath.output(str(arcaea_id) + "_recent"))


def get_song_info() -> list:
    with open(StaticPath.constants_json, "r", encoding="UTF-8") as f:
        return json.loads(f.read())
