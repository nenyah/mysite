from mongoengine import *


# ORM
class ItemInfo(Document):
    area = ListField(StringField())
    title = StringField()
    cates = ListField(StringField())
    price = FloatField()
    pub_date = StringField()
    url = StringField()
    look = StringField()
    time = IntField()

    meta = {
        'collection': 'item_info'
    }

