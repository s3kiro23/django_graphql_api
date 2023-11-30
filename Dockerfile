FROM python:3.11

ARG CONFIG

ARG APP_NAME="graphql_django_api"
ENV PYTHONPATH="/opt/$APP_NAME"

RUN mkdir -p /opt/$APP_NAME /var/log/$APP_NAME /var/run/$APP_NAME 
RUN apt update -y
RUN apt-get install -y cron
RUN apt-get install -y logrotate
WORKDIR /opt/$APP_NAME
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Installing App
COPY . .

# RUN crontab /etc/cron.d/root
RUN chown -R www-data:www-data /opt/$APP_NAME /var/log/$APP_NAME /var/run/$APP_NAME

WORKDIR /opt/$APP_NAME

RUN python manage.py collectstatic --noinput --clear
RUN chown -R www-data:www-data /opt/$APP_NAME/static_files
