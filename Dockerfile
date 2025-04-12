FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev build-essential pkg-config libssl-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]