FROM python:3.7-slim

LABEL author='Nezhinsky'

WORKDIR /app

COPY requirements.txt .

RUN apt-get update -y && apt-get upgrade -y && \
    pip install --upgrade pip &&  \
    pip install --root-user-action=ignore -r requirements.txt --no-cache-dir

COPY . .

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000