python manage.py migrate
python manage.py shell --command="`cat setup_djangoq.py`"
python manage.py runserver 0.0.0.0:8000 &
python manage.py qcluster