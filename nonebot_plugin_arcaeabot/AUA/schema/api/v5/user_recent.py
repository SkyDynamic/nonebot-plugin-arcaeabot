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
    "recent_score": [
        {
            "score": 9979350,
            "health": 100,
            "rating": 11.59675,
            "song_id": "melodyoflove",
            "modifier": 0,
            "difficulty": 2,
            "clear_type": 1,
            "best_clear_type": 3,
            "time_played": 1647570474485,
            "near_count": 2,
            "miss_count": 1,
            "perfect_count": 928,
            "shiny_perfect_count": 833
        },
        # More Score Info
    ],
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


class UserRecent(Base):
    account_info: AccountInfo
    recent_score: List[SongScore]
    songinfo: List[SongInfo]
