#!/bin/bash

# Create database
source src/config.py

# Create new database

psql -h "$host_name" -d "$database_name" -U "$role_name" -p "$port_name" -c "create database $new_database_name"

# Bugfix:
#https://stackoverflow.com/questions/56706631/psql-warning-extra-command-line-argument-from-ignored


# Create tables for new database, according to specifications in SQL file
psql -h $host_name -d $new_database_name -U $role_name -p $port_name -a -q -f src/setup/table_setup.sql