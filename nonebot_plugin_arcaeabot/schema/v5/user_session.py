from typing import Optional
from ..basemodel import Base


class Content(Base):
    session_info: str


class UserSession(Base):
    status: int
    message: Optional[str]
    content: Optional[Content]
