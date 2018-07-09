from collections import namedtuple
from datetime import datetime, timedelta
from math import log
from typing import List

from notifications_processor.event import Event

TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'
MAX_NOTIFICATIONS_PER_DAY = 4
SECONDS_PER_6H_PERIOD = 6 * 60 * 60
SMOOTHING_FACTOR = 0.5

Notification = namedtuple('Notification', 'notification_sent, timestamp_first_tour, tours, receiver_id, message')


class UserNotifications(object):

    def __init__(self, user_id):
        self.user_id = user_id
        self._events = []
        self._last_pushed_event_datetime = datetime.min
        self._delay_factor = 0

    def add_event_and_return_notifications(self, event: Event) -> List[Notification]:
        self._update_delay_factor(event.event_datetime)
        self._events.append(event)
        notifications = self._push_notifications()
        return notifications

    def _push_notifications(self) -> List[Notification]:
        notifications = []

        # Fix for first event notification
        if self._last_pushed_event_datetime == datetime.min:
            self._last_pushed_event_datetime = self._events[0].event_datetime

        # Check to see if the last added event datetime is after next calculated notification datetime
        # If it is, trigger notification bundling and return notification bundle (together with the last arrived event)
        if self._events[-1].event_datetime >= self._next_notification_datetime():
            notifications.append(
                Notification(notification_sent=self._next_notification_datetime().strftime(TIMESTAMP_FORMAT),
                             timestamp_first_tour=self._events[0].event_datetime.strftime(TIMESTAMP_FORMAT),
                             tours=str(len(self._events)),
                             receiver_id=self.user_id,
                             message=f'{self._friends_names()} went on a tour...'))

            # Set last event datetime from the list as _last_pushed_event_datetime
            self._last_pushed_event_datetime = self._events[-1].event_datetime
            # Clear list
            del self._events[:]

        return notifications

    def _update_delay_factor(self, event_datetime: datetime) -> None:
        """ After each added event, calculates new delay_factor as:
        delay_factor = delay_factor * SMOOTHING_FACTOR + correction * (1 - SMOOTHING_FACTOR)
        """
        correction = self._correction(event_datetime)
        self._delay_factor = self._delay_factor * SMOOTHING_FACTOR + correction * (1 - SMOOTHING_FACTOR)

    def _correction(self, event_datetime: datetime) -> float:
        """ Calculates correction as simple Heaviside step function (unit step function):
        f(x) = (0, x >= 6H;
                1, x < 6H)
        """
        time_delta = event_datetime - self._last_pushed_event_datetime
        seconds_delta = time_delta.total_seconds()
        if seconds_delta >= SECONDS_PER_6H_PERIOD:
            return 0
        else:
            return 1

    def _correction_logarithmic(self, event_datetime: datetime) -> float:
        """ Calculates correction as:
        f(x) = (1, x <= 6H/10;
                -log(x/6H), 6H/10 < x < 6H;
                0, x >= 6H)
        """
        time_delta = event_datetime - self._last_pushed_event_datetime
        seconds_delta = time_delta.total_seconds()
        if seconds_delta >= SECONDS_PER_6H_PERIOD:
            return 0
        elif seconds_delta <= SECONDS_PER_6H_PERIOD / 10:
            return 1
        else:
            return -log(seconds_delta / SECONDS_PER_6H_PERIOD)

    def _next_notification_datetime(self) -> datetime:
        """ Calculates and returns next notification datetime as:
        next_notification_datetime = last_pushed_event_datetime + delay_factor * SECONDS_PER_6H_PERIOD
        """
        return self._last_pushed_event_datetime + timedelta(seconds=SECONDS_PER_6H_PERIOD * self._delay_factor)

    def _friends_names(self) -> str:
        """ Util method for printing all unique friends names (sorted)
        in the form 'Friend1, Friend2, Friend3 ...'
        """
        Friend = namedtuple('Friend', 'friend_id, friend_name')
        friends = [Friend(friend_id=event.friend_id, friend_name=event.friend_name) for event in self._events]
        # Remove duplicates
        friends_set = set(friends)
        # Sorting names to make them deterministic (for testing purposes)
        friends_names = sorted([friend.friend_name for friend in friends_set])
        return ', '.join(friends_names)
