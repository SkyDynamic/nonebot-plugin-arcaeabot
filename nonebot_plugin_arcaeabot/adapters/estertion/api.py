# import websockets
# import ssl
# from brotli import decompress
# try:
#     import ujson as json
# except Exception:
#     import json
from typing import List, Dict

async def fetch_user_info(arcaea_id: str, recent_only: bool = False) -> List[Dict]:
    # 不推荐滥用Estertion的查分Api，如有需要请自行编写。
    pass