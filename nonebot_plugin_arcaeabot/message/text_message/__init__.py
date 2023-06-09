from ...schema import SongRandom, AUASongInfo
from ...resource_manager import assets_root, StaticPath
from nonebot.adapters.onebot.v11.message import MessageSegment
from ...config import StatusMsgDict
import random
import time


class TextMessage:
    help_message = MessageSegment.image(StaticPath.help)
    query_data = {}
    """
    {
        user_id(qq): {
            specific_number: num(int),
            reset_time: time(int),
            resp: SongRandom
            }
    }
    """

    @staticmethod
    def song_info_detail(data: SongRandom):
        if data.message:
            return StatusMsgDict.get(str(data.status))
        content = data.content
        song_name = content.song_info.name_en
        artist = content.song_info.artist
        difficulty = ["Past", "Present", "Future", "Beyond"][content.rating_class]
        cover_name = (
            f"{content.rating_class}.jpg"
            if content.song_info.jacket_override
            else "base.jpg"
        )
        image = "file:///" + str(assets_root / "song" / content.id / cover_name)
        result = "\n".join(
            [
                f"曲名: {song_name}[{difficulty}]",
                f"曲师: {artist}",
                f"曲绘: {content.song_info.jacket_designer}",
                f"时长: {'%02d:%02d' % divmod(content.song_info.time, 60)}",
                f"BPM: {content.song_info.bpm}",
                f"谱师: {content.song_info.chart_designer}",
                f"Note数: {content.song_info.note}",
                f"Rating: {content.song_info.rating/10}",
                f"隶属曲包: {content.song_info.set_friendly or content.song_info.set}",
                f"上线时间: { content.song_info.date.strftime('%Y-%m-%d')}",
            ]
        )
        result += "\n需要世界模式解锁" if content.song_info.world_unlock is True else ""
        result += "\n需要下载" if content.song_info.remote_download is True else ""
        return MessageSegment.image(image) + "\n" + result

    @staticmethod
    def ai_song_info_detail(data: SongRandom, user_id: str):
        if user_id not in TextMessage.query_data:
            TextMessage.query_data[user_id] = {}
            TextMessage.query_data[user_id]["specific_number"] = 5
            TextMessage.query_data[user_id]["reset_time"] = None
        if int(TextMessage.query_data.get(user_id).get("specific_number")) > 0:
            TextMessage.query_data[user_id]["resp"] = data
            randomtemplate = StaticPath.RandomTemplate
            random_text = str(random.choice(randomtemplate))
            content = data.content
            song_name = content.song_info.name_en
            artist = content.song_info.artist
            if "$songname$" in random_text:
                random_text = random_text.replace("$songname$", song_name)
            if "$artist$" in random_text:
                random_text = random_text.replace("$artist$", artist)
            TextMessage.query_data[user_id]["specific_number"] = (
                int(TextMessage.query_data.get(user_id).get("specific_number")) - 1
            )
            result = f'Ai酱：{random_text}\n剩余请求次数：{int(TextMessage.query_data.get(user_id).get("specific_number"))}'
            if TextMessage.query_data.get(user_id).get("specific_number") == 0:
                TextMessage.query_data[user_id]["reset_time"] = int(time.time() + 3599)
            return result
        else:
            TextMessage.query_data[user_id]["specific_number"] = (
                int(TextMessage.query_data.get(user_id).get("specific_number")) - 1
            )
            return f'无法处理更多请求。\n剩余请求次数：{int(TextMessage.query_data.get(user_id).get("specific_number"))}'

    @staticmethod
    def song_info(data: AUASongInfo, difficulty: int):
        if data.message:
            return StatusMsgDict.get(str(data.status))
        if difficulty + 1 > len(data.content.difficulties):
            return StatusMsgDict.get("-1001")
        if difficulty != -1:
            song_info = data.content.difficulties[difficulty]
            cover_name = (
                f"{difficulty}.jpg" if song_info.jacket_override else "base.jpg"
            )
            difficulty = ["Past", "Present", "Future", "Beyond"][difficulty]
            image = "file:///" + str(
                assets_root / "song" / data.content.song_id / cover_name
            )
            result = "\n".join(
                [
                    f"曲名: {song_info.name_en}[{difficulty}]",
                    f"曲师: {song_info.artist}",
                    f"曲绘: {song_info.jacket_designer}",
                    f"时长: {'%02d:%02d' % divmod(song_info.time, 60)}",
                    f"BPM: {song_info.bpm}",
                    f"谱师: {song_info.chart_designer}",
                    f"Note数: {song_info.note}",
                    f"Rating: {song_info.rating/10}",
                    f"隶属曲包: {song_info.set_friendly or song_info.set}",
                    f"上线时间: { song_info.date.strftime('%Y-%m-%d')}",
                ]
            )
            result += "\n需要世界模式解锁" if song_info.world_unlock is True else ""
            result += "\n需要下载" if song_info.remote_download is True else ""
            return MessageSegment.image(image) + "\n" + result

        image = "file:///" + str(
            assets_root / "song" / data.content.song_id / "base.jpg"
        )
        song_info_list = data.content.difficulties
        result = "\n".join(
            [
                f"Name: {song_info_list[0].name_en}",
                f"[Past]: {song_info_list[0].rating/10}",
                f"[Present]: {song_info_list[1].rating/10}",
                f"[Future]: {song_info_list[2].rating/10}",
            ]
        )
        result += (
            f"\n[Beyond]: {song_info_list[3].rating/10}"
            if len(song_info_list) > 3
            else ""
        )
        result += "\n获取详细信息请在添加难度后缀"
        return MessageSegment.image(image) + "\n" + result


class CalcMessage:
    @staticmethod
    def score(data: AUASongInfo, ptt: float, difficulty: int) -> str:
        if ptt >= 0:
            if difficulty + 1 > len(data.content.difficulties):
                return StatusMsgDict.get("-1001")
            if difficulty != -1:
                song_info = data.content.difficulties[difficulty]
                difficulty = ["Past", "Present", "Future", "Beyond"][difficulty]
                rating = song_info.rating / 10
                if ptt > rating + 2:
                    return "大于该曲目最高单曲Ptt, 不给予计算"
                if ptt == rating + 2:
                    score = f"10000000 - {10000000 + song_info.note}"
                elif ptt < rating + 1:
                    score = (ptt - rating) * 300000 + 9500000
                elif ptt >= rating + 1:
                    score = (ptt - rating - 1) * 200000 + 9800000
                result = "\n".join(
                    [
                        f"结算结果: ",
                        f"分数: {int(score)}",
                        f"计算的单曲ptt: {ptt}",
                        f"曲名: {song_info.name_en}",
                        f"难度: {difficulty}",
                    ]
                )
                return result
        return "?你想输入负数的ptt?"

    @staticmethod
    def ptt(data: AUASongInfo, score: int, difficulty: int) -> str:
        if score >= 0:
            if difficulty + 1 > len(data.content.difficulties):
                return StatusMsgDict.get("-1001")
            if difficulty != -1:
                song_info = data.content.difficulties[difficulty]
                difficulty = ["Past", "Present", "Future", "Beyond"][difficulty]
                rating = song_info.rating / 10
                if score > 10000000 + song_info.note:
                    return "大于该曲目理论分数, 不给予计算"
                if score >= 10000000:
                    ptt = rating + 2
                elif 9800000 <= score < 10000000:
                    ptt = rating + 1 + (score - 9800000) / 200000
                elif score < 9800000:
                    ptt = rating + (score - 9500000) / 300000
                result_ptt = round(ptt, 4)
                result = "\n".join(
                    [
                        f"结算结果: ",
                        # 以防它返回负数
                        f"单曲ptt: {result_ptt if result_ptt >= 0 else 0}",
                        f"计算的分数: {score}",
                        f"曲名: {song_info.name_en}",
                        f"难度: {difficulty}",
                    ]
                )
                return result
        return "?你想输入负数的分数?"
