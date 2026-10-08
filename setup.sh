export DOCKER_CLI_HINTS=false



echo "Setup container"
bash docker_setup.sh

sleep 3

echo "Setup role: developer"
bash role_setup.sh
sleep 1

echo "setup database"
bash db_setup.sh
sleep 1

echo "setup tables"
bash table_setup.sh
sleep 1

echo "Done!"