from .api import fetch_user_info
from ..utils import get_song_info


class ApiResult:
    @classmethod
    async def get_b30(self, arcaea_id: str, recent_only: bool = False):
        self.data = await fetch_user_info(arcaea_id, recent_only)
        self.name: str = self.data[2]["data"]["name"]
        self.character: int = self.data[2]["data"]["character"]
        self.is_char_uncapped: bool = self.data[2]["data"]["is_char_uncapped"]
        self.is_char_uncapped_override: bool = self.data[2]["data"]["is_char_uncapped_override"]
        self.rating: str = self.data[2]["data"]["rating"]
        self.score_info_list: list = self.data[3:]
        self.score_info_list.sort(
            key=lambda v: v["data"][0]["rating"], reverse=True)
        self.best_total: float = .0
        for i in (range(30) if len(self.score_info_list) >= 30 else range(len(self.score_info_list))):
            self.best_total += self.score_info_list[i]["data"][0]["rating"]
        self.best: float = self.best_total / 30
        self.recent: float = (self.rating / 100 - self.best * 0.75) / 0.25
        self.icon: str = (f"{self.character}u_icon.png"
                          if self.is_char_uncapped ^ self.is_char_uncapped_override
                          else f"{self.character}_icon.png")

    @classmethod
    async def get_recent(self, arcaea_id: str, recent_only: bool = True):
        self.data = (await fetch_user_info(arcaea_id, recent_only))[0]["data"]
        self.name: str = self.data["name"]
        self.character: int = self.data["character"]
        self.is_char_uncapped: bool = self.data["is_char_uncapped"]
        self.is_char_uncapped_override: bool = self.data["is_char_uncapped_override"]
        self.icon = (f"{self.character}u_icon.png"
                     if self.is_char_uncapped ^ self.is_char_uncapped_override
                     else f"{self.character}_icon.png")
        self.rating: int = self.data["rating"]
        self.song_id: str = self.data["recent_score"][0]["song_id"]
        self.song_info: list = get_song_info()
        self.song_name: str = self.song_info[0]["data"][self.song_id]["en"]
        self.author_name: str = self.song_info[1]["data"][self.song_id]
        self.difficulty: int = self.data["recent_score"][0]["difficulty"]
        self.score: int = self.data["recent_score"][0]["score"]
        self.shiny_perfect_count: int = self.data["recent_score"][0]["shiny_perfect_count"]
        self.perfect_count: int = self.data["recent_score"][0]["perfect_count"]
        self.near_count: int = self.data["recent_score"][0]["near_count"]
        self.miss_count: int = self.data["recent_score"][0]["miss_count"]
        self.health: int = self.data["recent_score"][0]["health"]
        self.song_rating: float = self.data["recent_score"][0]["rating"]
        self.constant: float = self.data["recent_score"][0]["constant"]
        self.full_character = (f"{self.character}u.png"
                               if self.is_char_uncapped ^ self.is_char_uncapped_override
                               else f"{self.character}.png")
