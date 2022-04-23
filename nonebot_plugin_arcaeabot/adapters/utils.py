from nonebot import get_driver
from ..config import Config
from typing import Optional


def adapter_selector() -> Optional[str]:
    plugin_config = Config.parse_obj(get_driver().config.dict())
    api_in_use = plugin_config.api_in_use
    if api_in_use:
        pass
    else:
        api_in_use = "AUA"
    return api_in_use


api_in_use = adapter_selector().upper()
if api_in_use == "AUA":
    from .aua.api import fetch_user_info
elif api_in_use == "ESTERTION":
    from .estertion.api import fetch_user_info
else:
    pass
