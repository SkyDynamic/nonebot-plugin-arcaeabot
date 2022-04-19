import ujson as json
with open("./data.json", "r", encoding="UTF-8") as f:
    data = json.loads(f.read())


class ApiResult:
    @classmethod
    def get_b30(self):
        self.data = data
        self.name: str = self.data["content"]["account_info"]["name"]
        self.character: int = self.data["content"]["account_info"]["character"]
        self.is_char_uncapped: bool = self.data["content"]["account_info"]["is_char_uncapped"]
        self.is_char_uncapped_override: bool = self.data["content"]["account_info"]["is_char_uncapped_override"]
        self.rating: int = 1058
        self.best: float = self.data["content"]["best30_avg"]
        self.recent: float = self.data["content"]["recent10_avg"]
        self.icon: str = (f"{self.character}u_icon.png"
                          if self.is_char_uncapped ^ self.is_char_uncapped_override
                          else f"{self.character}_icon.png")
        self.score_info_list = self.data["content"]["best30_list"]+self.data["content"]["best30_overflow"]
        self.song_name = "Fracture Ray"

    @classmethod
    def get_recent(self):
        self.data = data
        self.name: str = self.data["content"]["account_info"]["name"]
        self.character: int = self.data["content"]["account_info"]["character"]
        self.is_char_uncapped: bool = self.data["content"]["account_info"]["is_char_uncapped"]
        self.is_char_uncapped_override: bool = self.data["content"]["account_info"]["is_char_uncapped_override"]
        self.icon = (f"{self.character}u_icon.png"
                     if self.is_char_uncapped ^ self.is_char_uncapped_override
                     else f"{self.character}_icon.png")
        self.rating: int = self.data["content"]["account_info"]["rating"]
        self.song_id: str = self.data["content"]["recent_score"][0]["song_id"]
#        self.song_info: list = get_song_info()
#        self.song_name: str = self.song_info[0]["data"][self.song_id]["en"]
#        self.author_name: str = self.song_info[1]["data"][self.song_id]
        self.difficulty: int = self.data["content"]["recent_score"][0]["difficulty"]
        self.score: int = self.data["content"]["recent_score"][0]["score"]
        self.shiny_perfect_count: int = self.data["content"]["recent_score"][0]["shiny_perfect_count"]
        self.perfect_count: int = self.data["content"]["recent_score"][0]["perfect_count"]
        self.near_count: int = self.data["content"]["recent_score"][0]["near_count"]
        self.miss_count: int = self.data["content"]["recent_score"][0]["miss_count"]
        self.health: int = self.data["content"]["recent_score"][0]["health"]
        self.song_rating: float = self.data["content"]["recent_score"][0]["rating"]
#        self.constant: float = get_song_info()[2]["data"][self.song_id][self.data["content"]["recent_score"][0]["difficulty"]]
        self.full_character = (f"{self.character}u.png"
                               if self.is_char_uncapped ^ self.is_char_uncapped_override
                               else f"{self.character}.png")
