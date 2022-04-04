from PIL import Image
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.log import logger
from .assets import StaticPath
from .adapters.utils import (
    open_img, choice_ptt_background, DataText, adapter_selector,
    draw_text, player_time_format, song_time_format, get_song_info
)

api_in_use = adapter_selector().upper()
if api_in_use == "AUA":
    logger.info("将使用ArcaeaUnlimitedApi")
    from .adapters.aua.resolver import ApiResult
elif api_in_use == "ESTERTION":
    logger.info("将使用EstertionApi")
    from .adapters.estertion.resolver import ApiResult
else:
    logger.error("不支持的Api选项")


class UserArcaeaInfo:
    querying = list()

    @staticmethod
    def is_querying(arcaea_id: str) -> bool:
        return arcaea_id in UserArcaeaInfo.querying

    @staticmethod
    async def draw_best30_image(arcaea_id: str):
        UserArcaeaInfo.querying.append(arcaea_id)
        try:
            data = ApiResult()
            await data.get_b30(arcaea_id=arcaea_id)
        except Exception as e:
            UserArcaeaInfo.querying.remove(arcaea_id)
            return str(e)
        UserArcaeaInfo.querying.remove(arcaea_id)
        name: str = data.name
        rating: str = data.rating
        best: float = data.best
        recent: float = data.recent
        icon: str = data.icon
        score_info_list = data.score_info_list
        image = Image.new("RGBA", (1800, 3000))
        background = open_img(StaticPath.b30_background)
        image.alpha_composite(background)
        icon = open_img(StaticPath.select_image(
            "char", icon)).resize((250, 250))
        image.alpha_composite(icon, (175, 275))
        ptt_background = open_img(
            StaticPath.select_image("ptt", choice_ptt_background(rating))).resize((150, 150))
        image.alpha_composite(ptt_background, (300, 400))
        raw_ptt = str(round(rating/100, 2)).split(".")
        write_ptt_head = DataText(373, 490, 45, raw_ptt[0], StaticPath.exo_semibold, anchor="rs")
        image = draw_text(image, write_ptt_head, stroke_fill="Black", stroke_width=2)
        write_ptt_tail = DataText(373, 490, 35, "."+raw_ptt[1], StaticPath.exo_semibold, anchor="ls")
        image = draw_text(image, write_ptt_tail, stroke_fill="Black", stroke_width=2)
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
        for num, data in enumerate(score_info_list):
            if num == 30:
                break
            if num % 3 == 0:
                background_y += 240 if num != 0 else 0
                background_x = 30
            else:
                background_x += 600
            if api_in_use == "ESTERTION":
                data = data["data"][0]
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
                                      f'{get_song_info()[2]["data"][data["song_id"]][data["difficulty"]]:.1f}', StaticPath.exo_regular, anchor='rt')
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
    async def draw_recent_image(arcaea_id: str):
        UserArcaeaInfo.querying.append(arcaea_id)
        try:
            data = ApiResult()
            await data.get_recent(arcaea_id=arcaea_id)
        except Exception as e:
            UserArcaeaInfo.querying.remove(arcaea_id)
            return str(e)
        UserArcaeaInfo.querying.remove(arcaea_id)
        name: str = data.name
        character: int = data.character
        icon = data.icon
        rating: int = data.rating
        song_id: str = data.song_id
        song_name: str = data.song_name
        author_name: str = data.author_name
        difficulty: int = data.difficulty
        score: int = data.score
        shiny_perfect_count: int = data.shiny_perfect_count
        perfect_count: int = data.perfect_count
        near_count: int = data.near_count
        miss_count: int = data.miss_count
        health: int = data.health
        song_rating: float = data.song_rating
        constant: float = data.constant
        full_character = data.full_character
        image = Image.new("RGBA", (1280, 720))
        background = open_img(StaticPath.recent_background)
        image.alpha_composite(background)
        icon = open_img(StaticPath.select_image(
            "char", icon)).resize((130, 130))
        image.alpha_composite(icon, (575, -15))
        song_cover = open_img(StaticPath.select_image(
            "song", song_id, "base.jpg")).resize((375, 375))
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
            song_name.capitalize(), StaticPath.notosanscjksc_regular)
        image = draw_text(image, write_song_name)
        write_author = DataText(
            (640 - len(author_name) / 2 * 12), 165, 24,
            author_name.capitalize(), StaticPath.notosanscjksc_regular)
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
        raw_ptt = str(round(rating/100, 2)).split(".")
        write_ptt_head = DataText(690, 100, 30, raw_ptt[0], StaticPath.exo_semibold, anchor="rs")
        image = draw_text(image, write_ptt_head, stroke_fill="Black", stroke_width=2)
        write_ptt_tail = DataText(690, 100, 20, "."+raw_ptt[1], StaticPath.exo_semibold, anchor="ls")
        image = draw_text(image, write_ptt_tail, stroke_fill="Black", stroke_width=2)
        image.save(StaticPath.output(str(arcaea_id) + "_recent"))
        return MessageSegment.image("file:///"+StaticPath.output(str(arcaea_id) + "_recent"))
