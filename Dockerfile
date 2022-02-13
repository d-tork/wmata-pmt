FROM python:3.8.12-slim-buster
LABEL dev.d-tork.author="halpoins@gmail.com"

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

VOLUME /src

ENTRYPOINT ["python", "process.py"]
