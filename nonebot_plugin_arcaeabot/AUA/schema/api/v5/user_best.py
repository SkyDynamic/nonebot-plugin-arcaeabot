from typing import List


from ...basemodel import Base
from .song_score import SongScore
from .account_info import AccountInfo
from .song_info import SongInfo


"""
{
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
    "record": {
      "score": 9979257,
      "health": 100,
      "rating": 12.796285000000001,
      "song_id": "ifi",
      "modifier": 0,
      "difficulty": 2,
      "clear_type": 1,
      "best_clear_type": 5,
      "time_played": 1598919831344,
      "near_count": 5,
      "miss_count": 1,
      "perfect_count": 1570,
      "shiny_perfect_count": 1466
    },
    "songinfo": [
        {
            "name_en": "LunarOrbit -believe in the Espebranch road-",
            "name_jp": "白道、多希望羊と信じありく。",
            "artist": "Apo11o program ft. 大瀬良あい",
            "side": 1,
            "rating": 96,
        }
        # More Song Info
    ]
}
"""


class UserBest(Base):
    account_info: AccountInfo
    record: SongScore
    songinfo: List[SongInfo]
