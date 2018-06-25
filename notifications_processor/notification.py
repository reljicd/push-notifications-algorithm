from datetime import datetime


class Notification(object):

    def __init__(self, timestamp: datetime, friend_id: str, friend_name: str):
        self.timestamp = timestamp
        self.friend_id = friend_id
        self.friend_name = friend_name
