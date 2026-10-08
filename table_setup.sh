
# From: https://stackoverflow.com/questions/51553395/find-docker-file-path-according-to-container-id

# By writing:

# docker exec -it $container_name bash

# you get to a terminal inside the container.¨

# if you then write ls, you get the following:

# bin  boot  dev  docker-entrypoint-initdb.d  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var

# docker-entrypoint-initdb.d was mentioned in another solution.

# Then write exit to exit

# This one:
# https://stackoverflow.com/questions/34688465/how-do-i-run-a-sql-file-of-inserts-through-docker-run

# docker cp ./dump.sql pg_test:/docker-entrypoint-initdb.d/dump.sql
# docker exec -u postgres pg_test psql postgres postgres -f docker-entrypoint-initdb.d/dump.sql

# So that's probably what should be used here.
#docker-entrypoint-initdb.d

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



#docker cp ./localfile.sql containername:/container/path/file.sql
#docker exec -u postgresuser containername psql dbname postgresuser -f /container/path/file.sql
#docker run -v ./dump.sql:/docker-entrypoint-initdb.d/dump.sql pg_test
#docker ps
#Navigate inside your container where the log is present.

# docker exec -it ContainerName bash
#Locate your log within the container

#bash-4.2$ cd yourapplication/path/log/
#Exit Container

#  bash-4.2$ exit
#Copy to your Local location

# docker cp edd5064178db:yourapplication/path/log/request.log /your/local/location