from datetime import datetime

from ..basemodel import Base


class RecentInfo(Base):
    """
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
    """

    score: int


    song_id: str

    difficulty: int


    time_played: datetime