FROM python:3.8
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_PASSWORD=admin
ENV DJANGO_SUPERUSER_EMAIL=admin@admin.com
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN python manage.py migrate
RUN python manage.py shell --command="`cat setup_djangoq.py`"
RUN     python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
VOLUME ./app/db.sqlite3:/app/db.sqlite3
EXPOSE 8000:8000
CMD ["sh", "run_bash.sh"]