from datetime import datetime

from ..basemodel import Base


class RecentInfo(Base):
    """
    {
        "score": 9979350,
        "rating": 11.59675,
        "song_id": "melodyoflove",
        "difficulty": 2,
        "time_played": 1647570474485
    },
    """

    score: int
    rating: float
    song_id: str
    difficulty: int
    time_played: datetime
