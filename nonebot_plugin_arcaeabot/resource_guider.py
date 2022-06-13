from pathlib import Path

_root = Path(__file__).parent.absolute() / "resource"
_root.mkdir(exist_ok=True, parents=True)
assets_root = Path().absolute() / "data" / "arcaea" / "assets"
assets_root.mkdir(exist_ok=True, parents=True)


class StaticPath:
    b30_bg = _root / "b30" / "B30.png"
    divider = _root / "b30" / "Divider.png"
    mask = _root / "b30" / "mask.png"
    table = _root / "b30" / "table.png"
