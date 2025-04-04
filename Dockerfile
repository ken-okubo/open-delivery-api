FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install uvicorn[standard]

RUN apt-get update && apt-get install -y postgresql-client

COPY ./app /app/app
COPY ./alembic /app/alembic
COPY ./alembic.ini /app/


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--log-level", "debug"]