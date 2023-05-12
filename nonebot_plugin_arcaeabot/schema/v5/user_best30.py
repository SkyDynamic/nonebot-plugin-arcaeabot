from typing import List, Optional
from ..basemodel import Base
from .account_info import AccountInfo
from .song_info import SongInfo
from .score_info import ScoreInfo


class Content(Base):
    query_time: Optional[int]
    best30_avg: Optional[float]
    recent10_avg: Optional[float]
    account_info: Optional[AccountInfo]
    best30_list: Optional[List[ScoreInfo]]
    best30_song_info: Optional[List[SongInfo]]
    best30_overflow: Optional[List[ScoreInfo]]
    best30_overflow_song_info: Optional[List[SongInfo]]


class UserBest30(Base):
    status: int
    message: Optional[str]
    content: Optional[Content]
