from .matcher import arc
from .handler import b30_handler, assets_update_handler

arc.handle()(b30_handler)
arc.handle()(assets_update_handler)
