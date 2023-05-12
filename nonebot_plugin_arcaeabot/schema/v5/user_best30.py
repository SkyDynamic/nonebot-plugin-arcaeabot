from typing import List, Optional
from ..basemodel import Base
from .account_info import AccountInfo
from .song_info import SongInfo
from .score_info import ScoreInfo


class Content(Base):
    query_time: int
    best30_avg: float
    recent10_avg: float
    account_info: AccountInfo
    best30_list: List[ScoreInfo]
    best30_song_info: List[SongInfo]
    best30_overflow: List[ScoreInfo]
    best30_overflow_song_info: List[SongInfo]


class UserBest30(Base):
    status: int
    message: Optional[str]
    content: Optional[Content]
