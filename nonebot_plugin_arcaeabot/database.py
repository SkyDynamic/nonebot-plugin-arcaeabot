from nonebot.log import logger
from os import path
import peewee as pw
from .resource_manager import db_root

db = pw.SqliteDatabase(db_root / "user_data.db")


class UserInfo(pw.Model):
    user_qq = pw.IntegerField()
    arcaea_id = pw.CharField()

    class Meta:
        database = db
        primary_key = pw.CompositeKey("user_qq", "arcaea_id")


class ArcInfo(pw.Model):
    arcaea_name = pw.CharField()
    arcaea_id = pw.CharField()
    ptt = pw.IntegerField()

    class Meta:
        database = db
        primary_key = pw.CompositeKey("arcaea_name", "arcaea_id", "ptt")


class UserConfig(pw.Model):
    user_qq = pw.IntegerField()
    single_song_theme = pw.CharField()
    best30_theme = pw.CharField()

    class Meta:
        database = db
        primary_key = pw.CompositeKey("user_qq", "single_song_theme", "best30_theme")


if not path.exists(db_root / "user_data.db"):
    logger.info(f"创建数据库于 {db_root / 'user_data.db'}")
    db.connect()
    db.create_tables([UserInfo, ArcInfo, UserConfig])
    db.close()
else:
    db.connect()
    if "userinfo" not in db.get_tables():
        db.create_tables([UserInfo])
    if "userconfig" not in db.get_tables():
        db.create_tables([UserConfig])
    if "arcinfo" not in db.get_tables():
        db.create_tables([ArcInfo])
    db.close()
