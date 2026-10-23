
source src/configs/postgres_config.py



docker cp src/configs/tables/tableStations.sql  "$container_name":/docker-entrypoint-initdb.d/tableStations.sql

docker exec -it "$container_name" psql -h $host_name -d $new_database_name -U $role_name -p $port_name -a \
    -q -f docker-entrypoint-initdb.d/tableStations.sql


docker cp src/configs/tables/tableObservations.sql  "$container_name":/docker-entrypoint-initdb.d/tableObservations.sql

docker exec -it "$container_name" psql -h $host_name -d $new_database_name -U $role_name -p $port_name -a \
    -q -f docker-entrypoint-initdb.d/tableObservations.sql


docker cp src/configs/tables/tableStationParameters.sql  "$container_name":/docker-entrypoint-initdb.d/tableStationParameters.sql

docker exec -it "$container_name" psql -h $host_name -d $new_database_name -U $role_name -p $port_name -a \
    -q -f docker-entrypoint-initdb.d/tableStationParameters.sql


