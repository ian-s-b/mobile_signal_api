# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

WORKDIR /app

COPY . .
RUN pip3 install -r src/requirements.txt

WORKDIR /app/src

RUN python3 -m create_data

CMD [ "python3", "-m", "send_data_to_db" ]
