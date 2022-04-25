from nonebot.log import logger
from os import path
import peewee as pw
from ._RHelper import RHelper

root = RHelper()
db_path = root.database/("user_data.db")
db = pw.SqliteDatabase(db_path)


class UserInfo(pw.Model):
    user_qq = pw.IntegerField()
    arcaea_id = pw.CharField()
    arcaea_name = pw.CharField()

    class Meta:
        database = db
        primary_key = pw.CompositeKey("user_qq", "arcaea_id")


if not path.exists(db_path):
    logger.info(f"创建数据库于 {db_path}")
    db.connect()
    db.create_tables([UserInfo])
    db.close()
