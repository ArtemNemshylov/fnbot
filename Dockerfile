FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/opt/app

WORKDIR /opt/app

COPY requirements.txt /opt/app/requirements.txt

RUN pip install --upgrade pip && \
    pip install -r /opt/app/requirements.txt

COPY . /opt/app

RUN mkdir -p /data

WORKDIR /data

CMD ["python", "/opt/app/bot.py"]