from pathlib import Path

root = Path(__file__).parent.absolute() / "resource"
root.mkdir(exist_ok=True, parents=True)


class StaticPath:
    b30_bg = root / "b30" / "B30.png"


from PIL import Image

print(StaticPath.b30_bg)
res = Image.open(StaticPath.b30_bg).show()
