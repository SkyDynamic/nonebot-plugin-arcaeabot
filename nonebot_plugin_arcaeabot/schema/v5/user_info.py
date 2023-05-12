from typing import List, Optional
from ..basemodel import Base
from .song_info import SongInfo
from .score_info import ScoreInfo
from .account_info import AccountInfo


class Content(Base):
    account_info: AccountInfo
    recent_score: List[ScoreInfo]
    song_info: List[SongInfo]


class UserInfo(Base):
    status: int
    message: Optional[str]
    content: Optional[Content]
