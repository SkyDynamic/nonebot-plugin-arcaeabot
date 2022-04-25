"""
 - Author: DiheChen
 - Date: 2021-08-15 21:58:53
 - LastEditTime: 2021-08-18 03:10:39
 - LastEditors: DiheChen
 - Description: None
 - GitHub: https://github.com/Chendihe4975
"""
from os import path
import peewee as pw
from ._RHelper import RHelper

root = RHelper()
db = pw.SqliteDatabase(root/("data.db"))


class UserInfo(pw.Model):
    user_qq = pw.IntegerField()
    arcaea_id = pw.CharField()
    arcaea_name = pw.CharField()

    class Meta:
        database = db
        primary_key = pw.CompositeKey("user_qq", "arcaea_id")


if not path.exists(root("data.db")):
    db.connect()
    db.create_tables([UserInfo])
    db.close()
