#!/bin/bash

# Create database
source src/config.py
# Create new database

docker exec -it "$container_name" psql -h "$host_name" -d "$database_name" -U "$role_name" -p "$port_name" -c "create database $new_database_name"

# Bugfix:
#https://stackoverflow.com/questions/56706631/psql-warning-extra-command-line-argument-from-ignored


# Create tables for new database, according to specifications in SQL files:
#docker cp ./localfile.sql containername:/container/path/file.sql
#docker exec -u postgresuser containername psql dbname postgresuser -f /container/path/file.sql
#docker run -v ./dump.sql:/docker-entrypoint-initdb.d/dump.sql pg_test
# docker ps
#Navigate inside your container where the log is present.

# docker exec -it ContainerId bash
#Locate your log within the container

#bash-4.2$ cd yourapplication/path/log/
#Exit Container

#  bash-4.2$ exit
#Copy to your Local location

# docker cp edd5064178db:yourapplication/path/log/request.log /your/local/location


#docker exec -it "$container_name" psql -h $host_name -d $new_database_name -U $role_name -p $port_name -a -q -f src/setup/tableStations.sql

#docker exec -it "$container_name" psql -h $host_name -d $new_database_name -U $role_name -p $port_name -a -q -f src/setup/tableStationParameters.sql

#docker exec -it "$container_name"  psql -h $host_name -d $new_database_name -U $role_name -p $port_name -a -q -f src/setup/tableObservations.sql