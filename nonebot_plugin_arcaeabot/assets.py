from os import path

ASSETS = path.abspath(path.join(path.dirname(__file__), "assets"))

class StaticPath:
    database = path.join(ASSETS, "data.db")

    @staticmethod
    def output(name: str):
        return path.join(ASSETS, "output", f"{name}.png")
