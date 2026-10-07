#!/bin/bash
source src/config.py

docker run \
    --rm \
    --name "$container_name" \
    --env POSTGRES_PASSWORD="$superuser_password" \
    -p $port_setup \
    --detach postgres
# The variable {-d} ensures that program runs in detached mode, meaning it isn't necessary to open a new terminal window.

# The --rm flag ensures that it gets removed on stop.
#    --env POSTGRES_USER="$superuser_name" \ # This will make docker setup a default database *named* postgres user... in addition to postgres.
# Impossible to turn off it seems, kinda useless.