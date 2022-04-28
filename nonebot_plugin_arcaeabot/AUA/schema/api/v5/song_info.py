from typing import List


from ...basemodel import Base


"""
{
    "idx": 0,
    "id": "sayonarahatsukoi",
    "title_localized": {
    "en": "Sayonara Hatsukoi"
    },
    "artist": "REDSHiFT",
    "bpm": "178",
    "bpm_base": 178,
    "set": "base",
    "purchase": "",
    "audioPreview": 44494,
    "audioPreviewEnd": 76853,
    "side": 0,
    "bg": "",
    "date": 1487980800,
    "version": "1.0",
    "difficulties": [
    {
        "ratingClass": 0,
        "chartDesigner": "Nitro",
        "jacketDesigner": "",
        "rating": 1
    },
    {
        "ratingClass": 1,
        "chartDesigner": "Nitro",
        "jacketDesigner": "",
        "rating": 4
    },
    {
        "ratingClass": 2,
        "chartDesigner": "Toaster",
        "jacketDesigner": "",
        "rating": 7
    }
    ]
}
"""


class TitleLocalized(Base):
    en: str


class DifficultyInfo(Base):
    rating: int


class SongInfo(Base):
    idx: int
    id: str
    title_localized: TitleLocalized
    artist: str
    difficulties: List[DifficultyInfo]
