"""
 - Author: DiheChen
 - Date: 2021-08-15 22:00:59
 - LastEditTime: 2022-03-21 09:22:26
 - LastEditors: SEAFHMC
 - Description: None
 - GitHub: https://github.com/Chendihe4975
"""
from os import path

ASSETS = path.abspath(path.join(path.dirname(__file__), "assets"))


def check_rank(score: int):
    if score < 8600000:
        return "D"
    elif 8600000 <= score < 8900000:
        return "C"
    elif 8900000 <= score < 9200000:
        return "B"
    elif 9200000 <= score < 9500000:
        return "A"
    elif 9500000 <= score < 9800000:
        return "AA"
    elif 9800000 <= score < 9900000:
        return "EX"
    else:
        return "EX+"


def track_complete(score: int, lost_count: int) -> str:
    if not lost_count:
        return path.join(ASSETS, "recent", "clear_pure.png") if score > int(1e7) else path.join(ASSETS, "recent", "clear_full.png")
    return path.join(ASSETS, "recent", "clear_normal.png")


class StaticPath:
    database = path.join(ASSETS, "data.db")
    b30_background = path.join(ASSETS, "b30_bg.png")
    b30_score_background = path.join(ASSETS, "b30_score_bg.png")
    new_background = path.join(ASSETS, "new.png")
    recent_background = path.join(ASSETS, "recent", "recent_bg.png")
    hp_base = path.join(ASSETS, "recent", "hp_base.png")
    hp_grid = path.join(ASSETS, "recent", "hp_grid.png")
    hp_beyond_marker = path.join(ASSETS, "recent", "hp_beyond_marker.png")
    hp_grid = path.join(ASSETS, "recent", "hp_grid.png")
    res_scoresection_high = path.join(
        ASSETS, "recent", "res_scoresection_high.png")
    pure = path.join(ASSETS, "recent", "hit_pure.png")
    far = path.join(ASSETS, "recent", "hit_far.png")
    lost = path.join(ASSETS, "recent", "hit_lost.png")
    exo_regular = path.join(ASSETS, "font", "Exo-Regular.ttf")
    geosans_light = path.join(ASSETS, "font", "GeosansLight.ttf")
    NotoSansCJKsc_Regular = path.join(ASSETS, "font", "NotoSansCJKsc-Regular.otf")
    track_failed = path.join(ASSETS, "recent", "clear_normal.png")
    constants_json = path.join(ASSETS, "constants.json")

    @staticmethod
    def select_image(*args) -> str:
        return path.join(ASSETS, *args)

    @staticmethod
    def check_rank_background(score: int, failed: bool = False):
        img_name = f"grade_{check_rank(score).lower()}.png" if not failed else "grade_f.png"
        return path.join(ASSETS, "grade", img_name)

    @staticmethod
    def output(name: str):
        return path.join(ASSETS, "output", f"{name}.png")

    @staticmethod
    def is_failed(character: int, health: int, score: int, lost_count: int):
        def _check(x, y): return (x not in [
            7, 10, 14, 15, 28, 29, 35, 36, 37, 41, 42, 43] and y < 70) or (y == -1)
        return StaticPath.track_failed if _check(character, health) else track_complete(score, lost_count)

    @staticmethod
    def select_hp_bar_image(character: int):
        if character in [0, 9, 16, 20, 44]:
            return path.join(ASSETS, "recent", "hp_bar_easy.png")
        if character in [7, 10, 14, 15, 28, 29, 35, 36, 37, 41, 42, 43]:
            return path.join(ASSETS, "recent", "hp_bar_hard.png")
        return path.join(ASSETS, "recent", "hp_bar_limit_cover.png")

    @staticmethod
    def select_rating_image(score: int, failed: bool = False):
        img_name = f"grade_{check_rank(score).lower()}.png" if not failed else "grade_f.png"
        return path.join(ASSETS, "grade", img_name)
