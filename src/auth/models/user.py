import datetime

from mongoengine import *

from src.auth.model.group import Group


class User(Document):
    id = StringField(max_length=36, required=True)
    created = DateTimeField(default=datetime.datetime.utcnow)
    modified = DateTimeField(default=datetime.datetime.utcnow)
    group = ReferenceField(Group)
    active = BoolField(default=True)
