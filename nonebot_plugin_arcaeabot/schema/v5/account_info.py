from datetime import datetime
from ..basemodel import Base


class AccountInfo(Base):
    """
    {
        "code": "062596721",
        "name": "ToasterKoishi",
        "user_id": 4,
        "is_mutual": false,
        "is_char_uncapped_override": false,
        "is_char_uncapped": true,
        "is_skill_sealed": false,
        "rating": 1274,
        "character": 12
    }
    """

    code: str
    name: str
    user_id: int
    is_mutual: bool
    is_char_uncapped_override: bool
    is_char_uncapped: bool
    is_skill_sealed: bool
    rating: int
    character: int
