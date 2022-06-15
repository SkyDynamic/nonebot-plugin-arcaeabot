from datetime import datetime
from typing import List, Optional
from ..basemodel import Base
from .song_info import SongInfo
from .score_info import ScoreInfo


class AccountInfo(Base):
    code: str
    name: str
    user_id: int
    is_mutual: bool
    is_char_uncapped_override: bool
    is_char_uncapped: bool
    is_skill_sealed: bool
    rating: int
    join_date: datetime
    character: int


class Content(Base):
    account_info: AccountInfo
    recent_score: List[ScoreInfo]
    songinfo: List[SongInfo]


class UserInfo(Base):
    status: int
    message: Optional[str]
    content: Optional[Content]
