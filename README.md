# Komoot Challenge

## About

Backend Engineer (Algorithms)

Thank you for your application! We liked what we have seen so far from you and want to take the next
step: Inviting you to a small challenge that is quite close to what your tasks would look like.
Komoot is a platform for outdoor enthusiasts where you can follow your friends and like-minded
people to be informed about their latest tours. Some have only a few friends on komoot, others follow
hundreds of users. At the moment every time a tour is uploaded to komoot all followers get a push
notification on their mobile.

We identified that this can lead to a huge amount of notifications for some users. That’s not
acceptable as those users will be annoyed and eventually uninstall the app. We came up with the idea
of bundling notifications to reduce the amount of notifications we send. That means we need to wait a
bit to collect notifications until we can send those bundles. But we also know how important it is to
send notifications as soon as possible: users want to know about the tours of their friends as soon as
possible and start to talk about it.

Our goal is
* to not send more than 4 notifications a day to a user (should happen only few times)
* to keep sending delay minimal

Here is where we need your help to meet these contradictory requirements and find a clever and
optimized solution.

### Input
We prepared some sample data in a CSV file that simulates an incoming event stream. Every line
represents a new tour of a friend of which we want to inform a user.

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

### Requirements
Choose language and tools as your like. An excellent engineer should manage to do this challenge in a
few hours. Please send us the code, a small description and instruction how to setup and run your
application on a Mac or Linux machine. Please provide a command line parameter to specify the csv
file and print the csv result to stdout.
```bash
$> your_application https://s3.../backend/challenge/notifications.csv
```
Also provide additional information to help us understand how you came to this solution, where you
see strength, limitations and extensions. Finally just tell us what you’ve learned during the challenge

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