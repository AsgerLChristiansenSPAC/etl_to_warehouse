#!/bin/bash
source src/config.py

docker run --rm --name "$container_name" -e POSTGRES_USER="$superuser_name" -e POSTGRES_PASSWORD="$superuser_password" -p $port_setup -d postgres
# The variable {-d} ensures that program runs in detached mode, meaning it isn't necessary to open a new terminal window.

# Consider adding the --rm flag to ensure that it gets removed on stop.