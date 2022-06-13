from typing import Optional
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    aua_ua: Optional[str] = None
    aua_url: Optional[str] = None
    src_api_url: Optional[str] = None
