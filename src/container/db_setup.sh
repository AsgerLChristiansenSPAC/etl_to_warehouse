#!/bin/bash

# Create database
source src/config.py
# Create new database

docker exec -it "$container_name" psql -h "$host_name" -d "$database_name" -U "$role_name" -p "$port_name" -c "create database $new_database_name"

# Bugfix:
#https://stackoverflow.com/questions/56706631/psql-warning-extra-command-line-argument-from-ignored

