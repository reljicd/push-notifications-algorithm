from collections import defaultdict
from datetime import datetime

import fire
import pandas

from notifications_processor.notification import Notification
from notifications_processor.user_notifications import UserNotifications


def process_notifications(notifications_csv_path: str) -> None:

    user_notifications = defaultdict(UserNotifications)

    csv_df = pandas.read_csv(notifications_csv_path, header=None)

    for row in csv_df.itertuples():
        notification = Notification(timestamp=datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S'),
                                    friend_id=row[3],
                                    friend_name=row[4])
        user_notifications[row[2]].add_notification(notification)

    pass


if __name__ == '__main__':
    fire.Fire(process_notifications)
