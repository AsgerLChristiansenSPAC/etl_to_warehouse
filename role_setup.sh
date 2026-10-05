#!/bin/bash

# Create user that isn't superuser, which will be used for the rest of the project.
source src/config.py

psql -h $host_name -d $database_name -U $superuser_name -p $port_name -c \
"CREATE ROLE $role_name

WITH LOGIN PASSWORD $role_password

CREATEDB

;"