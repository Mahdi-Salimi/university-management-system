## Requirements

To run this program, you need the following:
- Python (version 3.11)
- PostgreSQL
- Redis
- Required python packages in `requirements.txt`
    - asgiref==3.7.2
    - celery==5.3.6
    - coverage==7.4.4
    - Django==5.0.2
    - django-filter==24.1
    - djangorestframework==3.15.0
    - djangorestframework-simplejwt==5.3.1
    - Markdown==3.6
    - pillow==10.2.0
    - psycopg==3.1.18
    - python-dotenv==1.0.1
    - redis==5.0.3
    - sqlparse==0.4.4
    - typing_extensions==4.10.0


## Configuration and Running

Follow these steps to configure and run the meeting room reservation system:

1. Clone this repository to your local machine:

```shell
git clone https://gitlab.com/group4-django-fall/samane-golestan.git
# or
git clone git@gitlab.com:group4-django-fall/samane-golestan.git
```
2. Create a virtual environment (optional but recommended) and activate the environment:

```shell
virtualenv django-env
# and
source django-env/bin/activate
```

3. Navigate to the project directory:
```shell
cd samane-golestan
```

4. Install the required dependencies using pip:
```shell
pip install -r requirements.txt
```


5. Make a copy of `.env_sample` and rename it to `.env` and edit the configuration as needed.
```env
SECRET_KEY=secret-key
DEBUG=True
DB_NAME=postgres
DB_USER=db_username
DB_PASSWORD=12345
DB_HOST=localhost
DB_PORT=5432
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2
```
6. Apply database migrations:
```shell
python manage.py makemigrations
python manage.py migrate
```

7. Run the command to create groups and permissions:
```shell
python manage.py create_perm_groups
```

8. Create a superuser account:
```shell
python manage.py createsuperuser
```

9. Start the server:
```
python manage.py runserver
```

### Running a Celery Worker:
Celery is a distributed task queue that facilitates the asynchronous execution of tasks in Python applications. It is commonly utilized for various purposes, including sending change password OTP (One-Time Password) codes to user email addresses. To start a Celery worker and utilize its capabilities, follow these steps:

1. Install Celery:

Ensure that Celery is installed in your Python environment. You can install it using pip:
```
pip install celery
```
2. Start a Celery Worker:

Open a terminal window, navigate to your project directory, and run the Celery worker using the celery command:
```
celery -A golestan worker --loglevel=info
celery -A golestan beat --loglevel=info
```

