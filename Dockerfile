FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /online_journal

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

RUN python manage.py collectstatic --no-input

RUN python manage.py migrate

RUN export DJANGO_SUPERUSER_PASSWORD=admin &&  \
    python manage.py createsuperuser --no-input --username admin --email admin@example.com

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]