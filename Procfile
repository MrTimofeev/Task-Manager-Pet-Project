release: python manage.py migrate
web: gunicorn --chdir task_manager task_manager.wsgi --log-file -