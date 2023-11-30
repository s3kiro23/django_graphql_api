#!/bin/bash

source /opt/graphql_django_api/config.ini

echo "AWS Region: $AWS_REGION"
echo "AWS Account ID: $AWS_ACCOUNT_ID"

# Replace these values with your specific ones
APP_NAME="graphql_django_api"
APP_PATH="/opt/dev_custom/projects/$APP_NAME/"

cd $APP_PATH
cd deploy/prod

#git stash
#git checkout main
#git pull origin main

docker pull $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$APP_NAME:latest

RUN_DIR="/var/run/$APP_NAME"
LOG_DIR="/var/dev_data/$APP_NAME/log"
DATA_DIR="/var/dev_data/$APP_NAME"

if [ ! -d $RUN_DIR ]; then
    mkdir -p $RUN_DIR
    chown -R www-data:www-data $RUN_DIR
fi

if [ ! -d $LOG_DIR ]; then
    mkdir -p $LOG_DIR
    chown -R www-data:www-data $LOG_DIR
fi

if [ ! -d $DATA_DIR ]; then
    mkdir -p $DATA_DIR
    chown -R www-data:www-data $DATA_DIR
fi

docker-compose down -v
docker-compose up -d

VOLUME_DIR=`docker volume inspect --format '{{ .Mountpoint }}' $APP_NAME'_static'`
TARGET_DIR='/var/www/'$APP_NAME'_static'

echo "Symlink : $VOLUME_DIR to $TARGET_DIR"

if [ -d $VOLUME_DIR ]; then
    if [[ -L $TARGET_DIR ]]; then
        rm $TARGET_DIR
    fi
    ln -s $VOLUME_DIR $TARGET_DIR
fi
