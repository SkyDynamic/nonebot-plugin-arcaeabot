from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    src_api_url: str = "http://107.182.17.60:17777/api/"
