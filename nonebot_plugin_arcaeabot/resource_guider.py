from pathlib import Path

resource_root = Path(__file__).parent.absolute() / "resource"
resource_root.mkdir(exist_ok=True, parents=True)

assets_root = Path().absolute() / "data" / "arcaea" / "assets"
assets_root.mkdir(exist_ok=True, parents=True)

db_root = Path().absolute() / "data" / "arcaea"


class StaticPath:
    b30_bg = resource_root / "b30" / "B30.png"
    divider = resource_root / "b30" / "Divider.png"
    mask = resource_root / "b30" / "mask.png"
    table = resource_root / "b30" / "table.png"
