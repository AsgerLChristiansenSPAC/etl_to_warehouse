
source src/config.py



docker cp src/setup/tableStations.sql  "$container_name":/docker-entrypoint-initdb.d/tableStations.sql

docker exec -it "$container_name" psql -h $host_name -d $new_database_name -U $role_name -p $port_name -a \
    -q -f docker-entrypoint-initdb.d/tableStations.sql


docker cp src/setup/tableObservations.sql  "$container_name":/docker-entrypoint-initdb.d/tableObservations.sql

docker exec -it "$container_name" psql -h $host_name -d $new_database_name -U $role_name -p $port_name -a \
    -q -f docker-entrypoint-initdb.d/tableObservations.sql


docker cp src/setup/tableStationParameters.sql  "$container_name":/docker-entrypoint-initdb.d/tableStationParameters.sql

docker exec -it "$container_name" psql -h $host_name -d $new_database_name -U $role_name -p $port_name -a \
    -q -f docker-entrypoint-initdb.d/tableStationParameters.sql


