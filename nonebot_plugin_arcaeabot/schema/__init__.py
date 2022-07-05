from .v5.user_info import UserInfo
from .v5.user_best30 import UserBest30
from .v5.song_info import SongInfo
from .v5.score_info import ScoreInfo
from .v5.account_info import AccountInfo
from .v5.user_best import UserBest
from .v5.song_random import SongRandom
from .v5.aua_song_info import AUASongInfo


def diffstr2num(diff: str):
    diff_dict = {
        "PAST": 0,
        "PST": 0,
        "PRESENT": 1,
        "PRS": 1,
        "FUTURE": 2,
        "FTR": 2,
        "BEYOND": 3,
        "BYD": 3,
        "ALL": -1,
    }
    return diff_dict.get(diff, None)
