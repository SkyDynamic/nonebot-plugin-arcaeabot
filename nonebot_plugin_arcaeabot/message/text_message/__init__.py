from ...schema import SongRandom, AUASongInfo
from ...resource_manager import assets_root, StaticPath
from nonebot.adapters.onebot.v11.message import MessageSegment
import random
import time

class TextMessage:
    help_message = MessageSegment.image(StaticPath.help)
    query_data = {}

    '''
    {
        user_id(qq): {
            specific_number: num(int),
            reset_time: time(int)
            resp: SongRandom
            }
    }
    '''

    @staticmethod
    def song_info_detail(data: SongRandom):
        if error_message := data.message:
            return error_message
        content = data.content
        song_name = content.songinfo.name_en
        artist = content.songinfo.artist
        difficulty = ["Past", "Present", "Future", "Beyond"][content.ratingClass]
        cover_name = (
            f"{content.ratingClass}.jpg"
            if content.songinfo.jacket_override
            else "base.jpg"
        )
        image = "file:///" + str(assets_root / "song" / content.id / cover_name)
        result = "\n".join(
            [
                f"曲名: {song_name}[{difficulty}]",
                f"曲师: {artist}",
                f"曲绘: {content.songinfo.jacket_designer}",
                f"时长: {'%02d:%02d' % divmod(content.songinfo.time, 60)}",
                f"BPM: {content.songinfo.bpm}",
                f"谱师: {content.songinfo.chart_designer}",
                f"Note数: {content.songinfo.note}",
                f"Rating: {content.songinfo.rating/10}",
                f"隶属曲包: {content.songinfo.set_friendly or content.songinfo.set}",
                f"上线时间: { content.songinfo.date.strftime('%Y-%m-%d')}",
            ]
        )
        result += "\n需要世界模式解锁" if content.songinfo.world_unlock is True else ""
        result += "\n需要下载" if content.songinfo.remote_download is True else ""
        return MessageSegment.image(image) + "\n" + result

    @staticmethod
    def ai_song_info_detail(data: SongRandom, user_id: str):
        if user_id not in TextMessage.query_data:
            TextMessage.query_data[user_id] = {}
            TextMessage.query_data[user_id]['specific_number'] = 5
            TextMessage.query_data[user_id]['reset_time'] = None
        if int(TextMessage.query_data.get(user_id).get('specific_number')) > 0:
            TextMessage.query_data[user_id]['resp'] = data
            randomtemplate = StaticPath.RandomTemplate
            random_text = str(random.choice(randomtemplate))
            content = data.content
            song_name = content.songinfo.name_en
            artist = content.songinfo.artist
            if '$songname$' in random_text:
                random_text = random_text.replace('$songname$', song_name)
            if '$artist$' in random_text:
                random_text = random_text.replace('$artist$', artist)
            TextMessage.query_data[user_id]['specific_number'] = int(TextMessage.query_data.get(user_id).get('specific_number')) - 1
            result = f'Ai酱：{random_text}\n剩余请求次数：{int(TextMessage.query_data.get(user_id).get("specific_number"))}'
            if TextMessage.query_data.get(user_id).get('specific_number') == 0:
                TextMessage.query_data[user_id]['reset_time'] = int(time.time() + 3599)
            return result
        else:
            TextMessage.query_data[user_id]['specific_number'] = int(TextMessage.query_data.get(user_id).get('specific_number')) - 1
            return f'无法处理更多请求。\n剩余请求次数：{int(TextMessage.query_data.get(user_id).get("specific_number"))}'

    @staticmethod
    def song_info(data: AUASongInfo, difficulty: int):
        if error_message := data.message:
            return error_message
        if difficulty + 1 > len(data.content.difficulties):
            return "this song has no beyond level"
        if difficulty != -1:
            songinfo = data.content.difficulties[difficulty]
            cover_name = f"{difficulty}.jpg" if songinfo.jacket_override else "base.jpg"
            difficulty = ["Past", "Present", "Future", "Beyond"][difficulty]
            image = "file:///" + str(
                assets_root / "song" / data.content.song_id / cover_name
            )
            result = "\n".join(
                [
                    f"曲名: {songinfo.name_en}[{difficulty}]",
                    f"曲师: {songinfo.artist}",
                    f"曲绘: {songinfo.jacket_designer}",
                    f"时长: {'%02d:%02d' % divmod(songinfo.time, 60)}",
                    f"BPM: {songinfo.bpm}",
                    f"谱师: {songinfo.chart_designer}",
                    f"Note数: {songinfo.note}",
                    f"Rating: {songinfo.rating/10}",
                    f"隶属曲包: {songinfo.set_friendly or songinfo.set}",
                    f"上线时间: { songinfo.date.strftime('%Y-%m-%d')}",
                ]
            )
            result += "\n需要世界模式解锁" if songinfo.world_unlock is True else ""
            result += "\n需要下载" if songinfo.remote_download is True else ""
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