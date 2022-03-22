"""
 - Author: DiheChen
 - Date: 2021-08-15 22:00:39
 - LastEditTime: 2021-08-18 01:09:17
 - LastEditors: DiheChen
 - Description: None
 - GitHub: https://github.com/Chendihe4975
"""
import websockets
import ssl
from brotli import decompress
from typing import List, Dict
try:
    import ujson as json
except Exception:
    import json


async def fetch_user_info(arcaea_id: int, recent_only: bool = False) -> List[Dict]:
    async with websockets.connect("wss://arc.estertion.win:616/", ssl=ssl._create_unverified_context()) as websocket:
        await websocket.send(str(arcaea_id))
        result = list()
        while (data := await websocket.recv()) != "bye":
            if isinstance(data, bytes):
                if recent_only and (user_info := json.loads(decompress(data)))["cmd"] == "userinfo":
                    return [user_info]
                result.append(json.loads(decompress(data)))
        return result
