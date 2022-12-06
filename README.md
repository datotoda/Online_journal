# Django Classroom

Online journal for teachers. Used Django, crispy, bootstrap.

---

# Documentations

- [Django Documentation](https://www.djangoproject.com/)
  
- [Crispy Documentation](https://django-crispy-forms.readthedocs.io/en/latest/)

- [Bootstrap Documentation](https://getbootstrap.com/)

# Docker

[Docker hub](https://hub.docker.com/r/datotoda/online_journal)

```bash 
docker run -d -p 80:8000 datotoda/online_journal
```

#### default admin user:

username: admin

password: admin

# Local Setup

## Environment

Install requirements

``$ pip install -r requirements.txt``

## Database

Create sqlite3 database

``$ python manage.py migrate``

Create admin account

``$ python manage.py createsuperuser``

# Run

Run Django server

``$ python manage.py runserver 80``
