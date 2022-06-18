from typing import Optional, List
from ..basemodel import Base
from .song_info import SongInfo


class Content(Base):
    song_id: str
    difficulties: List[SongInfo]


class AUASongInfo(Base):
    status: int
    message: Optional[str]
    content: Optional[Content]
