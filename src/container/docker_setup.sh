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

# Note: Specifying POSTGRES_USER automatically creates a default database with that name, in addition to the default postgres.
# Hence, POSTGRES_USER isnt specified, defaulting to "postgres"