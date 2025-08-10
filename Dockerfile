FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
RUN chmod 0777 /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x ./bootstrap/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/app/bootstrap/entrypoint.sh"]
