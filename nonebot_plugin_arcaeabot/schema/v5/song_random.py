from ..basemodel import Base
from .song_info import SongInfo
from typing import Optional


class Content(Base):
    id: str
    ratingClass: int
    songinfo: SongInfo


class SongRandom(Base):
    status: Optional[int]
    message: Optional[str]
    content: Optional[Content]
