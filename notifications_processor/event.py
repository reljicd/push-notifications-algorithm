from datetime import datetime


class Event(object):

    def __init__(self, event_datetime: datetime, friend_id: str, friend_name: str):
        self.event_datetime = event_datetime
        self.friend_id = friend_id
        self.friend_name = friend_name
