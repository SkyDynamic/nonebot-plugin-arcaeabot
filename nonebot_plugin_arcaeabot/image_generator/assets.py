from .._RHelper import RHelper


root = RHelper()


class StaticPath:
    B30_bg = root.assets("B30.png")
    mask = root.assets("mask.png")
    table = root.assets("table.png")
    divider = root.assets("Divider.png")
    song_dir = root.assets.song
    diff_dir = root.assets.diff
    char_dir = root.assets.char
    ptt_dir = root.assets.ptt
    andrea = root.assets.Fonts/("Andrea.otf")
    exo_andrea_light = root.assets.Fonts/("Exo Andrea Light.otf")
    exo_medium = root.assets.Fonts/("Exo-Medium.ttf")
    kazesawa_light = root.assets.Fonts/("Kazesawa-Light.ttf")
    kazesawa_regular = root.assets.Fonts/("Kazesawa-Regular.ttf")
    notosanscjksc_regular = root.assets.Fonts/("NotoSansCJKsc-Regular.otf")
    slst_json = root.assets/("slst.json")
