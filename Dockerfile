FROM python:3.11-slim

RUN apt-get update && apt-get install -y build-essential netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

WORKDIR app/

COPY entrypoint.sh /entrypoint.sh

COPY .env .env

RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]