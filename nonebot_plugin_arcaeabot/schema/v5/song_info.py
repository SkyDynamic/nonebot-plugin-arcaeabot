from datetime import datetime
from typing import Optional
from ..basemodel import Base


class SongInfo(Base):
    """
    {
        "name_en": "LunarOrbit -believe in the Espebranch road-",
        "name_jp": "白道、多希望羊と信じありく。",
        "artist": "Apo11o program ft. 大瀬良あい",
        "bpm": "192",
        "bpm_base": 192.0,
        "set": "base",
        "set_friendly": "Arcaea",
        "time": 141,
        "side": 1,
        "world_unlock": true,
        "remote_download": false,
        "bg": "mirai_conflict",
        "date": 1535673600,
        "version": "1.7",
        "difficulty": 18,
        "rating": 96,
        "note": 1058,
        "chart_designer": "月刊Toaster",
        "jacket_designer": "hideo",
        "jacket_override": false,
        "audio_override": false
    }
    """

    name_en: str
    name_jp: Optional[str]
    artist: str
    bpm: str
    bpm_base: int
    set: str
    set_friendly: Optional[str]
    time: int
    side: int
    world_unlock: bool
    remote_download: bool
    bg: str
    date: datetime
    version: float
    difficulty: int
    rating: int
    note: int
    chart_designer: str
    jacket_designer: str
    jacket_override: bool
    audio_override: bool
