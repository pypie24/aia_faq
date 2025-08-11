FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
RUN chmod 0777 /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod -R 0777 /app

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "5000", "--reload", "--workers", "4"]
