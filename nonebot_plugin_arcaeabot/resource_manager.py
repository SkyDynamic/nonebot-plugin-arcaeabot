from pathlib import Path
from os import path

import json

resource_root = Path(__file__).parent.absolute() / "resource"
resource_root.mkdir(exist_ok=True, parents=True)

assets_root = Path().absolute() / "data" / "arcaea" / "assets"
assets_root.mkdir(exist_ok=True, parents=True)

db_root = Path().absolute() / "data" / "arcaea"


class StaticPath:
    # B30 Image
    b30_bg = resource_root / "b30" / "B30.png"
    divider = resource_root / "b30" / "Divider.png"
    mask = resource_root / "b30" / "mask.png"
    table = resource_root / "b30" / "table.png"
    ptt = resource_root / "b30" / "Ptt.png"
    char_dir = assets_root / "char"
    song_dir = assets_root / "song"
    ptt_dir = resource_root / "ptt"
    diff_dir = resource_root / "diff"
    # Recent Image
    rawv3bg_0 = resource_root / "recent" / "RawV3Bg_0.png"
    rawv3bg_1 = resource_root / "recent" / "RawV3Bg_1.png"
    arcaea_0 = resource_root / "recent" / "arcaea_style" / "arcaea_0.png"
    arcaea_style_dir = resource_root / "recent" / "arcaea_style"
    track_failed = resource_root / "recent" / "clear_normal.png"
    # Font
    exo_medium = resource_root / "font" / "Exo-Medium.ttf"
    roboto_regular = resource_root / "font" / "Roboto-Regular.ttf"
    andrea = resource_root / "font" / "Andrea.otf"
    kazesawa_regular = resource_root / "font" / "Kazesawa-Regular.ttf"
    exo_semibold = resource_root / "font" / "Exo-SemiBold.ttf"
    exo_regular = resource_root / "font" / "Exo-Regular.ttf"
    nsc_regular = resource_root / "font" / "NotoSansCJK-Regular.otf"
    # Grade
    grade_a = resource_root / "grade" / "grade_a.png"
    grade_aa = resource_root / "grade" / "grade_aa.png"
    grade_b = resource_root / "grade" / "grade_b.png"
    grade_c = resource_root / "grade" / "grade_c.png"
    grade_d = resource_root / "grade" / "grade_d.png"
    grade_ex = resource_root / "grade" / "grade_ex.png"
    grade_ex_plus = resource_root / "grade" / "grade_ex+.png"
    grade_l = resource_root / "grade" / "grade_l.png"
    # Help
    help = resource_root / "help.png"
    # Random
    RandomTemplate = json.load(
        open(resource_root / "RandomTemplate.json", "r", encoding="utf8")
    )

    # Method
    def select_image(*args) -> str:
        return path.join(str(assets_root), *args)

    @staticmethod
    def is_failed(type: str):
        return resource_root / "recent" / f"{type}.png"
