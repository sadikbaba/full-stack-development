FROM python:3.14-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/backend

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000"]

CMD [ "--workers", "1", "--graceful-timeout", "30", "config.wsgi:application"]