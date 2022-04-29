from .._RHelper import RHelper
from os import path


root = RHelper()
ASSETS = root.assets


def track_complete(score: int, lost_count: int) -> str:
    if not lost_count:
        return (
            root.assets.recent / ("clear_pure.png")
            if score > int(1e7)
            else root.assets.recent / ("clear_full.png")
        )
    return root.assets.recent / ("clear_normal.png")


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


class StaticPath:
    # B30
    B30_bg = root.assets / ("B30.png")
    mask = root.assets / ("mask.png")
    table = root.assets / ("table.png")
    divider = root.assets / ("Divider.png")
    song_dir = root.assets.song
    diff_dir = root.assets.diff
    char_dir = root.assets.char
    ptt_dir = root.assets.ptt
    andrea = root.assets.font / ("Andrea.otf")
    exo_andrea_light = root.assets.font / ("Exo Andrea Light.otf")
    exo_medium = root.assets.font / ("Exo-Medium.ttf")
    kazesawa_light = root.assets.font / ("Kazesawa-Light.ttf")
    kazesawa_regular = root.assets.font / ("Kazesawa-Regular.ttf")
    notosanscjksc_regular = root.assets.font / ("NotoSansCJKsc-Regular.otf")

    # Recent
    recent_background = root.assets.recent / ("recent_bg.png")
    recent_background = root.assets.recent / ("recent_bg.png")
    hp_base = root.assets.recent / ("hp_base.png")
    hp_grid = root.assets.recent / ("hp_grid.png")
    hp_beyond_marker = root.assets.recent / ("hp_beyond_marker.png")
    hp_grid = root.assets.recent / ("hp_grid.png")
    res_scoresection_high = root.assets.recent / ("res_scoresection_high.png")
    pure = root.assets.recent / ("hit_pure.png")
    far = root.assets.recent / ("hit_far.png")
    lost = root.assets.recent / ("hit_lost.png")
    track_failed = root.assets.recent / ("clear_normal.png")
    exo_regular = root.assets.font / ("Exo-Regular.ttf")
    geosans_light = root.assets.font / ("GeosansLight.ttf")
    notosanscjksc_regular = root.assets.font / ("NotoSansCJKsc-Regular.otf")
    exo_semibold = root.assets.font / ("Exo-SemiBold.ttf")

    # Function
    @staticmethod
    def select_image(*args) -> str:
        return path.join(str(ASSETS), *args)

    @staticmethod
    def check_rank_background(score: int, failed: bool = False):
        img_name = (
            f"grade_{check_rank(score).lower()}.png" if not failed else "grade_f.png"
        )
        return root.assets.grade / img_name

    @staticmethod
    def is_failed(character: int, health: int, score: int, lost_count: int):
        def _check(x, y):
            return (
                x not in [7, 10, 14, 15, 28, 29, 35, 36, 37, 41, 42, 43] and y < 70
            ) or (y == -1)

        return (
            StaticPath.track_failed
            if _check(character, health)
            else track_complete(score, lost_count)
        )

    @staticmethod
    def select_hp_bar_image(character: int):
        if character in [0, 9, 16, 20, 44]:
            return root.assets.recent / ("hp_bar_easy.png")
        if character in [7, 10, 14, 15, 28, 29, 35, 36, 37, 41, 42, 43]:
            return root.assets.recent / ("hp_bar_hard.png")
        return root.assets.recent / ("hp_bar_limit_cover.png")

    @staticmethod
    def select_rating_image(score: int, failed: bool = False):
        img_name = (
            f"grade_{check_rank(score).lower()}.png" if not failed else "grade_f.png"
        )
        return root.assets.grade / img_name
