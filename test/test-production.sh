#!/bin/bash

if [ "$DATABASE_HOST" = "" ]
then
	sql_host="localhost"
else
	sql_host="$DATABASE_HOST"
fi

if [ "$DATABASE_PORT" = "" ]
then
	sql_port="3306"
else
	sql_port="$DATABASE_PORT"
fi

mysql --host=${sql_host} --port=${sql_port} -u348proj -p movielist < test-production.sql | tee  test-production.out


