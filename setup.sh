export DOCKER_CLI_HINTS=false



echo "Setup container"
bash src/container/docker_setup.sh

sleep 3

echo "Setup role: developer"
bash src/container/role_setup.sh
sleep 1

echo "Setup database"
bash src/container/db_setup.sh
sleep 1

echo "Setup tables"
bash src/container/table_setup.sh
sleep 1

echo "Done!"