FROM python:3.9.11-slim-bullseye
LABEL dev.d-tork.author="halpoins@gmail.com"

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["python", "process.py"]
