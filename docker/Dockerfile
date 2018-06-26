FROM python:3.6

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY notifications_processor notifications_processor
COPY test test
COPY input input
COPY utils utils

RUN mkdir output

ENV PYTHONPATH $PYTHONPATH:$(pwd)

ENTRYPOINT ["python"]
CMD ["notifications_processor/main.py", "--events_csv_path=input/notifications_short.csv", "--print_to_stdout=True"]