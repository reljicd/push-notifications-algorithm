# Push Notifications Algorithm

## About the Problem

Some users have only a few friends, others follow
hundreds of users. At the moment every time an event by a user is uploaded all followers get a push
notification on their mobile.

This can lead to a huge amount of notifications for some users. That’s not
acceptable as those users will be annoyed and eventually uninstall the app. The idea
is to bundle notifications to reduce the amount of notifications to send. That means to wait a
bit to collect notifications until we can send those bundles. But it is also important to
send notifications as soon as possible: users want to know about the events of their friends as soon as
possible and start to talk about it.

The goal is
* to not send more than 4 notifications a day to a user (should happen only few times)
* to keep sending delay minimal

### Input
Sample data in a CSV file that simulates an incoming event stream. Every line
represents a new event of a friend of which we want to inform a user.

```
timestamp user_id friend_id friend_name
2018-02-14 11:50:02, EB96305EADU2, 84BE9DC3BFLL, Matthew
2018-02-14 11:50:02, 0B4E1F74A818, 84BE9DC3BFLL, Matthew
2018-02-14 11:50:05, 0B4E1F74A818, E670587FFC18, Jonathan
```

### Output
The output should be also a CSV file which contains all (bundled) notifications
```
notification_sent timestamp_first_tour tours receiver_id message
2018-02-14 11:50:02, 2018-02-14 11:50:02, 1, EB96305EADU2, Matthew went on a tour
2018-02-14 11:57:21, 2018-02-14 11:50:02, 2, 0B4E1F74A818, Matthew and 1 other went on a
tour
```

## Solution

The problem is finding the optimal solution to two conflicting constraints:
1. To not send more than 4 messages per day.
2. But to send messages as soon as you can.

Based on the constraints, we have 2 edge cases:
* On one end of the spectrum we have constant stream of high frequency events that are very close together (minutes, seconds...). 
For this case it is obvious that we need to cache them and then every 6h bundle them together and publish them.
In this case delay since the first event in this group should be 6h.

```delay = 6h```

```delay_factor = 1```

* On the other end of the spectrum we have low frequency events that are more than 6h apart. 
For this case we can publish those events as soon as they arrive. 
In this case the delay since the first event in this group should be 0

```delay = 0```

```delay_factor = 0```

Based on the first edge case I introduced this ***6h interval***.
Based on that interval I introduced delay factor:

```delay = delay_factor * 6h```

In the real system number of friends per user should not change too rapidly too often. That means that frequency of the events per user should be fairly consistent.
In other words, for a user with very few friends events should be low frequent and for this user those events should be published as soon as they arrive. For this user high frequency events should be anomaly, not a rule.
For a user with great number of friends events should be high frequent and for this user those events would be bundled and published every 6h. For this user low frequency events should be anomaly, not a rule.
But those anomalies could occur in real systems.

Because of this I am taking into account both history of the delays as well as frequency of the most recent events. 
In order to take history of the delays into account, I calculate delay factor as exponential average (https://en.wikipedia.org/wiki/Exponential_smoothing):

```delay_factor = delay_factor * smoothing_factor + correction * (1 - smoothing_factor)```

That way if there is anomaly in the frequency of the events it will not make too much of the impact on the delay. 
But if the frequency really changed delay will exponentially adapt to this.

Now I need some way to calculate correction.
I choose Heaviside unit step function (https://en.wikipedia.org/wiki/Heaviside_step_function):
```
f(x) = (0, x >= 6H;
        1, x < 6H)
```
where x is time delta between last arrived event and the last pushed event.
This function is based on those two edge cases from the beginning. 
In other words, for each event that arrived less than 6h after the previous correction is 1.
For each event that arrived more than 6h after the previous correction is 0.

I also experimented with this function (I assumed step function is too discontinuous and maybe smoother logarithmic correction for values will yield better results):
```
f(x) = (1, x <= 6H/10;
        -log(x/6H), 6H/10 < x < 6H;
        0, x >= 6H)
```
but found that Heaviside step function works much better.

With these parameters I can easily calculate time when next message should be published:

```next_notification_time = last_pushed_event_time + delay```

Now each time a new event for a user arrives I update correction and delay factor values and then calculate what should be the next notification time. 
If that time is before that event's arrival time I bundle all the piled events together with that last arrived event and push them.
If it is not I push the event to the list of the piled up events. 

Also, first event for each user is published straight away (delay_factor starts at 0).
For each subsequent event I calculate the new correction, delay factor and the next notification time.

For tuning and optimization I wrote a lot of tests that covered several edge cases. 
While running tests I tuned both smoothing factor and correction function.
I chose in the end 0.5 for smoothing factor and Heaviside function for correction function.

Also take note, in my code I used different names for some of these parameters:
delay_factor - exp_average
smoothing_factor -  EXP_AVERAGE_WEIGHT
6H -  SECONDS_PER_6H_PERIOD 
next_notification_time - next_notification_datetime
last_pushed_event_time -  last_pushed_event_datetime

## Prerequisites

\[Optional\] Install virtual environment:

```bash
$> sudo apt install python3-pip
$> pip3 install virtualenv
$> python3 -m virtualenv venv
```

Activate virtual environment:

On macOS and Linux:
```bash
$> source venv/bin/activate
```

On Windows:
```bash
$> .\venv\Scripts\activate
```

\[Optional\] Install dependencies (in a new virtual environment):
```bash
$> pip install -r requirements.txt
```

Add project directory to PYTHONPATH
```bash
$> export PYTHONPATH=$PYTHONPATH:$(pwd)
```

## How to run

### Default

```bash
$> python notifications_processor/main.py --events_csv_path=input/notifications_short.csv --print_to_stdout=True
```

#### Helper script

It is possible to run all of the above with helper script:

```bash
$> chmod +x scripts/activate_venv_and_run.sh
$> scripts/activate_venv_and_run_python.sh notifications_processor/main.py --events_csv_path=input/notifications_short.csv --print_to_stdout=True
```

### Docker

It is possible to run application using Docker:

Build Docker image:
```bash
$> sudo docker build -t reljicd/komoot_challenge -f docker/Dockerfile .
```

Run Docker container:
```bash
$> sudo docker run --rm -i reljicd/komoot_challenge notifications_processor/main.py --events_csv_path=input/notifications_short.csv --print_to_stdout=True
```

#### Docker helper script

It is possible to run all of the above with helper script:

```bash
$> chmod +x scripts/run_docker.sh
$> sudo scripts/run_docker.sh notifications_processor/main.py --events_csv_path=input/notifications_short.csv --print_to_stdout=True
```

### Tests

#### Default
Activate virtual environment:

On macOS and Linux:
```bash
$> source venv/bin/activate
```

On Windows:
```bash
$> .\venv\Scripts\activate
```

Running tests:
```bash
$> export PYTHONPATH=$PYTHONPATH:$(pwd)
$> python -m pytest
```

#### Helper script

It is possible to run all of the above with helper script:

```bash
$> chmod +x scripts/activate_venv_and_run.sh
$> scripts/activate_venv_and_run_python.sh -m pytest
```

#### Docker

It is also possible to run tests using Docker:

Build the Docker image:
```bash
$> sudo docker build -t reljicd/komoot_challenge -f docker/Dockerfile .
```

Run the Docker container:
```bash
$> sudo docker run --rm -i reljicd/komoot_challenge -m pytest
```

#### Docker helper script

It is possible to run all of the above with helper script:

```bash
$> chmod +x scripts/run_docker.sh
$> sudo scripts/run_docker.sh -m pytest
```