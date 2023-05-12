from ..basemodel import Base
from .song_info import SongInfo
from typing import Optional


class Content(Base):
    id: str
    rating_class: int
    song_info: SongInfo


class SongRandom(Base):
    status: Optional[int]
    message: Optional[str]
    content: Optional[Content]
