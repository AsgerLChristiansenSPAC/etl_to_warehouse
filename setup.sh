export DOCKER_CLI_HINTS=false

echo "Setup container"
bash src/postgres_setup/docker_setup.sh

sleep 3

echo "Setup role:"
bash src/postgres_setup/role_setup.sh
sleep 1

echo "Setup database"
bash src/postgres_setup/db_setup.sh
sleep 1

echo "Setup tables"
bash src/postgres_setup/table_setup.sh
sleep 1

echo "Done!"