import os
from os import path


ROOT = path.abspath(path.join(path.dirname(__file__)))


class RHelper(str):
    def __init__(self, path: str = None) -> None:
        if not path:
            self.__rpath = ROOT
        else:
            self.__rpath = path

    def __getattr__(self, key):
        path = os.path.join(self.__rpath, key)
        path = os.path.normpath(path)
        return __class__(path)

    def __floordiv__(self, key):
        path = os.path.join(self.__rpath, key)
        path = os.path.normpath(path)
        return __class__(path)

    def __truediv__(self, key):
        path = os.path.join(self.__rpath, key)
        path = os.path.normpath(path)
        return __class__(path)

    def __add__(self, key):
        path = os.path.join(self.__rpath, key)
        path = os.path.normpath(path)
        return __class__(path)

    def __call__(self, path, *paths):
        key = os.path.join(path, *paths)
        path = os.path.join(self.__rpath, key)
        path = os.path.normpath(path)
        return __class__(path)
