from typing import List


from ...basemodel import Base


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


class SongInfo(Base):
    name_en: str
    artist: str
    side: int
    rating: int
