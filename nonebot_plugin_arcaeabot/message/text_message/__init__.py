from ...schema import SongRandom, AUASongInfo
from ...resource_manager import assets_root, StaticPath
from nonebot.adapters.onebot.v11.message import MessageSegment


class TextMessage:
    help_message = MessageSegment.image(StaticPath.help)

    @staticmethod
    def song_info_detail(data: SongRandom):
        if error_message := data.message:
            return error_message
        content = data.content
        difficulty = ["Past", "Present", "Future", "Beyond"][content.ratingClass]
        cover_name = "3.jpg" if content.songinfo.jacket_override else "base.jpg"
        image = "file:///" + str(assets_root / "song" / content.id / cover_name)
        result = "\n".join(
            [
                f"曲名: {content.songinfo.name_en}[{difficulty}]",
                f"曲师: {content.songinfo.artist}",
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
    def song_info(data: AUASongInfo, difficulty: int):
        if error_message := data.message:
            return error_message
        if difficulty != -1:
            songinfo = data.content.difficulties[difficulty]
            difficulty = ["Past", "Present", "Future", "Beyond"][difficulty]
            cover_name = "3.jpg" if songinfo.jacket_override else "base.jpg"
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
