from .matcher import arc
from .handler import (
    b30_handler,
    assets_update_handler,
    pre_handler,
    bind_handler,
    info_handler,
    recent_handler,
    best_handler,
    help_handler,
    random_handler,
    song_handler,
    default_handler,
    preview_handler,
)

arc.handle()(pre_handler)
arc.handle()(b30_handler)
arc.handle()(recent_handler)
arc.handle()(best_handler)
arc.handle()(song_handler)
arc.handle()(preview_handler)
arc.handle()(bind_handler)
arc.handle()(info_handler)
arc.handle()(assets_update_handler)
arc.handle()(help_handler)
arc.handle()(random_handler)
arc.handle()(default_handler)
