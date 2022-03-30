from pydantic import BaseModel, Extra
from typing import Optional


class Config(BaseModel, extra=Extra.ignore):
    src_api_url: Optional[str] = None
    aua_url: Optional[str] = None
    aua_ua: Optional[str] = None
    api_in_use: Optional[str] = None
