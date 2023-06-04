from typing import Optional
from ..basemodel import Base
import re

class Content(Base):
    session_info: Optional[str]


class UserSession(Base):
    status: int
    message: Optional[str]
    content: Optional[Content]

def get_message(session_msg: str) -> str:
    result_msg = None
    if 'session querying, queried charts' in session_msg:
        result_msg = '会话查询中...查询铺面数量：' + str(re.findall(r'^session querying, queried charts: (.+?)', session_msg)[0])
    elif 'session waiting for account, account count' in session_msg:
        result_msg = '会话正在等待用户...当前查询用户数量：' + str(re.findall(r"^session waiting for account, account count: (.+?)", session_msg)[0])
    return result_msg if result_msg else session_msg