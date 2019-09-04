import datetime

from mongoengine import *


class User(Document):
    id = StringField(max_length=36, required=True)
    created = DateTimeField(default=datetime.datetime.utcnow)
    modified = DateTimeField(default=datetime.datetime.utcnow)
    active = BooleanField(default=True)
