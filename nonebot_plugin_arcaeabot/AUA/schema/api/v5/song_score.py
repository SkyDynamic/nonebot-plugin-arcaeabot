from datetime import datetime

from ...basemodel import Base


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


class SongScore(Base):
    score: int
    health: int
    rating: float
    song_id: str
    modifier: int
    difficulty: int
    clear_type: int
    best_clear_type: int
    time_played: int
    near_count: int
    miss_count: int
    perfect_count: int
    shiny_perfect_count: int
