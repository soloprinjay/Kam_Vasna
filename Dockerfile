FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Install dependencies including PostgreSQL client and netcat
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /code/

RUN chmod +x /code/entrypoint.sh

ENTRYPOINT ["/code/entrypoint.sh"]
