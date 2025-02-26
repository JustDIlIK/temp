FROM python:3.12

WORKDIR /app

COPY req.txt .

RUN pip install -r req.txt

COPY . .

CMD alembic upgrade head && gunicorn main:app --workers 3 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000 --forwarded-allow-ips='*'
