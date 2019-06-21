python manage.py migrate
python manage.py collectstatic --no-input
/opt/conda/envs/django_motion/bin/gunicorn -w 4 -b 0.0.0.0:8000 app.wsgi:application