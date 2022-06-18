from typing import List, Optional


from ..basemodel import Base
from .score_info import ScoreInfo
from .account_info import AccountInfo
from .song_info import SongInfo


class Content(Base):
    account_info: AccountInfo
    record: ScoreInfo
    songinfo: List[SongInfo]


class UserBest(Base):
    status: int
    message: Optional[str]
    content: Optional[Content]
