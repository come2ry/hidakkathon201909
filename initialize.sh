#!/bin/sh

export MYSQL_PWD=hidakkathon

initialize () {
    set -e
    echo Initialize...
    mysql -u hidakkathon -e 'CREATE DATABASE IF NOT EXISTS sugori_rendez_vous'
    mysql -u hidakkathon sugori_rendez_vous < mysql/01-schema.sql
    gzip -dc mysql/02-data.sql.gz | mysql -u hidakkathon sugori_rendez_vous
    echo Done!!!
}

LOG=`initialize 2>&1`
if [ $? -eq 0 ]; then
    echo "Status: 200 OK"
else
    echo "Status: 500 Internal Server Error"
fi
echo

echo "$LOG"

