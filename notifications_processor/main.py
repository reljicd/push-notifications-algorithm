from datetime import datetime

import fire
import pandas

from notifications_processor.event import Event
from notifications_processor.user_notifications import UserNotifications, TIMESTAMP_FORMAT

OUTPUT_PATH = 'output/notifications.csv'


def process_notifications(events_csv_path: str,
                          output_path: str = OUTPUT_PATH,
                          print_to_stdout: bool = False) -> None:
    # Dict of UserNotifications objects, where keys are user_id
    user_notifications_dict = {}

    input_df = pandas.read_csv(events_csv_path, header=None)

    notifications = []

    # Parse rows and add each users event to corresponding UserNotifications object in user_notifications_dict
    for row in input_df.itertuples():
        user_id = row[2]
        event = Event(event_datetime=datetime.strptime(row[1], TIMESTAMP_FORMAT),
                      friend_id=row[3],
                      friend_name=row[4])
        if user_id not in user_notifications_dict:
            user_notifications_dict[user_id] = UserNotifications(user_id)

        # Collect all notifications
        notifications.extend(user_notifications_dict[user_id].add_event_and_return_notifications(event))

    if print_to_stdout:
        for notification in notifications:
            print(notification)

    # Export to CSV
    output_df = pandas.DataFrame(notifications)
    output_df.to_csv(output_path, index=False, header=True)


if __name__ == '__main__':
    fire.Fire(process_notifications)
