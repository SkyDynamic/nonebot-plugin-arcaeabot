from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    src_api_url: str = "http://107.182.17.60:17777/api/"
    aua_url: str = "SECRET"
    aua_ua: str = "SECRET"
    api_in_use: str = "aua"
