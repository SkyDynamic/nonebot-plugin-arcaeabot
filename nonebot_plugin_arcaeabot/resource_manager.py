from pathlib import Path
from os import path

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
    track_failed = resource_root / "recent" / "clear_normal.png"
    # Font
    exo_medium = resource_root / "font" / "Exo-Medium.ttf"
    roboto_regular = resource_root / "font" / "Roboto-Regular.ttf"
    andrea = resource_root / "font" / "Andrea.otf"
    kazesawa_regular = resource_root / "font" / "Kazesawa-Regular.ttf"
    exo_semibold = resource_root / "font" / "Exo-SemiBold.ttf"
    exo_regular = resource_root / "font" / "Exo-Regular.ttf"
    # Help
    help = resource_root / "help.png"

    # Method
    def select_image(*args) -> str:
        return path.join(str(assets_root), *args)

    @staticmethod
    def is_failed(type: str):
        return resource_root / "recent" / f"{type}.png"