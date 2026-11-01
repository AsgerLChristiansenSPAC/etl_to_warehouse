# ETL Process from DMI Climate Data API to PostgreSQL database + own API

This project is in two parts.

 - 1. An ETL-pipeline from DMI's Climate Data api into a postgres database. The project is written with DMI in mind. Work on making the code more easily configurable to other APIs is not finished.

 - 2. A simple API setup to allow others to extract data from the postgres database.

## Running the ETL process

*First*, consult the installation guide below, to make sure appropriate software and python packages are installed.

*Secondly*, write a **local configuration file** for the postgres database.
The config file must be called 'src/configs/postgres_config.py', and it specifies the following:

- Connection information to the database (port, database name, etc.)
- New database name (the program assumes it will not be working in the default database "postgres")
- Superuser login information. The superuser is used as sparingly as possible, mainly to set up the new database, and to create a new role with fewer priviliges.
- Login credentials for the new role.

See "postgres_config-template" below.


*Third*, start Docker desktop.

*Fourth*, run the following command in a bash terminal:

```
bash setup.sh
```

to setup a docker container, create a new database and a new role, and create three tables: stations, observations and stationParameters.

*Fifth*, run:

```
bash etl.sh
```

You will be prompted for the following input. In both cases, entering "d" means selecting a default option.

- Which DMI stationId you wish to extract data from. At present, the program is limited to extracting data from one station at a time. Default ID is "06070", located at Aarhus Lufthavn.

- Which time period you wish to extract data from. Correct input is in the format '%Y-%m-%dT%H:%M:%SZ/%Y-%m-%dT%H:%M:%SZ'. For example, the default input is:
2026-01-09T03:00:00Z/2026-01-09T11:00:00Z

**NOTE:** It is most likely easier to change the default datetime range than to manually input it. Default query variables are contained in *src/configs/etl_config.py*.

Additionally, you will be prompted to enter the new role password specified in your local config file whenever data is loaded into a table. Usually, this is three times during the process.

With all of this done, you should have loaded data from the specified station and timeframe into the postgres database.

### Running the API

Assuming the docker container with the database is currently running, the API endpoint can be hosted by running:

```
bash api.sh
```

from the terminal, which causes uvicorn to run the app contained in *api.py*. Go to the specified host adress to access the endpoint.

The api is simple and proof-of-concept. It contains endpoints for each of the database tables. Some of the tables have query parameters.

*/stations* (Query-parameters: stationId)

*/stationparameters* (Query-parameters: None)

*/observations* (Query-parameters: stationId, parameterId)

## Installation Guide and Requirements

### Python
This program was developed in Python 3.13.15.

### Docker and Postgres Image

The program assumes Docker Desktop is installed locally and running, allowing for the execution of "docker run ..." -style commands from terminal.

Additionally, the program requires a postgreSQL image for docker, to allow the creation of a postgres database in a container.
The image version used in this program is 18.6, at the time of writing (01/11/2026) tagged as "latest": https://hub.docker.com/_/postgres/

### Python package dependencies

#### Quick dependency installation

The following command:

```
bash install_packages.sh
```

installs the necessary dependencies **without** specifying package version (as most likely, later versions of these packages will still work).

For manual installation, see "Dependency Details" below.

#### Dependency Details

The following packages are required. The version specified is the one used at the time of development. Other versions may also work.

Unless otherwise specified, installation of these packages can be done normally through a 'pip install [package_name]' command.


*psycopg*, Version 3.3.6: https://psycopg.org/

- Used for connecting to the postgres database and executing SQL statements.
To install: pip install "psycopg[binary]"

Quoting from psycopg.org: "The [binary] extra bundles a pre-compiled C extension so no PostgreSQL client libraries need to be installed separately." (01/11/2026)

*fastapi*, Version 0.156.7, https://github.com/fastapi/fastapi

- Used for coding the API endpoints, query methods, etc.

*uvicorn*, version 0.54.0, https://uvicorn.dev/

- Used for actually running and hosting the API.

To install: pip install "uvicorn[standard]"

*pydantic*, version 2.14.1 (https://github.com/pydantic/pydantic)

- Required by fastapi, and should be installed alongside it. Nonetheless highlighted here because pydantic models are important for the API portion of the program.

*requests*, Version 2.34.2


## postgres_config Template:

Use the following template to write your own configuration file.

The file should be located in *src/configs/* and be named *postgres_config.py*.

**TEMPLATE FOR CONFIG FILE. REMEMBER TO REPLACE DEFAULT PASSWORDS!**

```
#Docker connectivity info
container_name="container_name"
host_name="localhost"
port_setup="5432:5432"
port_name="5432"

#Superuser information:
superuser_name="postgres"
superuser_password="Y0urP@sswordH3re"
database_name="postgres"

#New database name*
new_database_name="database name here"
role_name="role name here"
role_password="'n3wP@ssw0rdHere'"

```

## Authors

Asger L. Christiansen