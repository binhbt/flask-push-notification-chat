from .db import db
import datetime

class NotiMessage(db.Document):
    group_ids = db.ListField(db.StringField(),  unique=False)
    message = db.StringField(required=False, unique=False)
    mtype = db.StringField(required=False, unique=False)
    status = db.StringField(required=False, unique=False)
    url = db.StringField(required=False, unique=False)
    created = db.DateTimeField(default=datetime.datetime.utcnow)
    def to_json(self):
        return {"group_ids": self.group_ids,
                "message": self.message,
                "mtype": self.mtype,
                "status": self.status,
                "url": self.url,
                'id': str(self.id)}    

class UserReadMessage(db.Document):
    client_id = db.StringField(required=True, unique=False)
    message_id = db.StringField(required=True, unique=False)
    created = db.DateTimeField(default=datetime.datetime.utcnow)
    def to_json(self):
        return {"client_id": self.client_id,
                "message_id": self.message_id,
                "created": self.created,
                'id': str(self.id)}  