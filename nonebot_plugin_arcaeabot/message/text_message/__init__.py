from ...schema import SongRandom, AUASongInfo
from ...resource_manager import assets_root
from nonebot.adapters.onebot.v11.message import MessageSegment


class TextMessage:
    help_message = "\n".join(
        [
            "/arc bind <arcaea id> 进行绑定",
            "/arc info 查看绑定信息",
            "/arc recent 查询上一次游玩记录",
            "/arc b30 查询 best 30 记录",
            "/arc assets_update 更新曲绘与立绘资源",
            "/arc best <曲名> [难度] 查询单曲最高分",
            "/arc song <曲名> [难度] 查询信息",
            "/arc random [难度] 随机指定难度的歌曲",
            "/arc random [难度min] [难度max] 随机指定难度区间的歌曲",
            "/arc preview <曲名> [难度] 查看单曲铺面预览",
        ]
    )

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
                f"隶属曲包: {content.songinfo.set_friendly}",
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
                    f"隶属曲包: {songinfo.set_friendly}",
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