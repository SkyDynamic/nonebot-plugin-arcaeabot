import peewee as pw
from .._RHelper import RHelper

root = RHelper()

db = pw.SqliteDatabase(root.database / ("arcsong.db"))


class alias(pw.Model):
    sid = pw.IntegerField()
    alias = pw.CharField()

    class Meta:
        database = db
        primary_key = pw.CompositeKey("sid", "alias")
