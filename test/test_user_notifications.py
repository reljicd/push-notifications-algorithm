from datetime import datetime
from typing import Dict

import pytest

from notifications_processor.event import Event
from notifications_processor.user_notifications import UserNotifications, TIMESTAMP_FORMAT
from utils.utils_for_testing import filter_tests_by_category, load_tests

TEST_USER_NOTIFICATIONS_CONFIG = 'test/fixtures/test_user_notifications.yaml'


@pytest.mark.parametrize('case_params',
                         filter_tests_by_category(
                             tests=load_tests(file=TEST_USER_NOTIFICATIONS_CONFIG),
                             cat='add_event_and_return_notifications'))
def test_add_event_and_return_notifications(case_params: Dict) -> None:
    user_notifications = UserNotifications(user_id=case_params['user_id'])

    pushed_notifications = []

    for event in case_params['events']:
        pushed_notifications.extend(user_notifications.add_event_and_return_notifications(
            Event(event_datetime=datetime.strptime(event['event_datetime'], TIMESTAMP_FORMAT),
                  friend_id=event['friend_id'],
                  friend_name=event['friend_name'])))

    for pushed_notification, expected_notification in zip(pushed_notifications, case_params['notifications']):
        assert pushed_notification.timestamp_first_tour == expected_notification['timestamp_first_tour']
        assert pushed_notification.tours == expected_notification['tours']
        assert pushed_notification.receiver_id == expected_notification['receiver_id']
        assert pushed_notification.message == expected_notification['message']


@pytest.mark.parametrize('case_params',
                         filter_tests_by_category(
                             tests=load_tests(file=TEST_USER_NOTIFICATIONS_CONFIG),
                             cat='notifications_count_per_day'))
def test_notifications_count_per_day(case_params: Dict) -> None:
    user_notifications = UserNotifications(user_id=case_params['user_id'])

    pushed_notifications = []

    for event in case_params['events']:
        pushed_notifications.extend(user_notifications.add_event_and_return_notifications(
            Event(event_datetime=datetime.strptime(event['event_datetime'], TIMESTAMP_FORMAT),
                  friend_id=event['friend_id'],
                  friend_name=event['friend_name'])))

    assert len(pushed_notifications) == case_params['notifications_count']
