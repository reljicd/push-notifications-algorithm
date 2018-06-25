from notifications_processor.notification import Notification


class UserNotifications(object):

    def __init__(self):
        self.notifications = []
        self.last_notification = None

    def add_notification(self, notification: Notification) -> None:
        self.notifications.append(notification)

    def push_notifications(self):
        raise NotImplemented
