from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    src_api_url: str = "http://127.0.0.1:17777/api/"
