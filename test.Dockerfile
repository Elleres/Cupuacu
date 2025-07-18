FROM python:3.11-slim

RUN apt-get update && apt-get install -y build-essential netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY test_entrypoint.sh /test_entrypoint.sh

RUN chmod +x /test_entrypoint.sh

CMD ["/test_entrypoint.sh"]