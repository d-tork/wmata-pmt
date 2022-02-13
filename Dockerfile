FROM python:3.8.12-slim-buster
LABEL dev.d-tork.author="halpoins@gmail.com"

RUN mkdir /app
COPY requirements.txt /app
RUN pip3 install -r /app/requirements.txt

VOLUME /src

ENTRYPOINT ["python", "/src/process.py"]
