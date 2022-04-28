from typing import List



from ...basemodel import Base
from .song_score import SongScore
from .account_info import AccountInfo
from .song_info import SongInfo


"""
{
    "best30_avg": 12.707672500000001,
    "recent10_avg": 12.836982499999998,
    "account_info": {
      "code": "062596721",
      "name": "ToasterKoishi",
      "user_id": 4,
      "is_mutual": false,
      "is_char_uncapped_override": false,
      "is_char_uncapped": true,
      "is_skill_sealed": false,
      "rating": 1274,
      "join_date": 1487816563340,
      "character": 12
    },
    "best30_list": [
      {
        "score": 9956548,
        "health": 100,
        "rating": 13.082740000000001,
        "song_id": "grievouslady",
        "modifier": 0,
        "difficulty": 2,
        "clear_type": 1,
        "best_clear_type": 5,
        "time_played": 1614911430950,
        "near_count": 7,
        "miss_count": 3,
        "perfect_count": 1440,
        "shiny_perfect_count": 1376
      },
      # More Score Info  
    ],
    "best30_overflow": [
      {
        "score": 9993863,
        "health": 100,
        "rating": 12.469315,
        "song_id": "ikazuchi",
        "modifier": 0,
        "difficulty": 2,
        "clear_type": 1,
        "best_clear_type": 2,
        "time_played": 1584913642898,
        "near_count": 0,
        "miss_count": 1,
        "perfect_count": 1346,
        "shiny_perfect_count": 1287
      },
      # More Score Info
    ],
    "best30_songinfo": List[SongInfo],
    "best30_overflow_songinfo": List[SongInfo]
}
"""


class UserBest30(Base):
    best30_avg: float
    recent10_avg: float
    account_info: AccountInfo
    best30_list: List[SongScore]
    best30_overflow: List[SongScore]
    best30_songinfo: List[SongInfo]
    best30_overflow_songinfo: List[SongInfo]
