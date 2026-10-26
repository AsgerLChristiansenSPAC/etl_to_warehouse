# Project Title

This project is in two parts.

 - 1. A simple proof-of-concept ETL-pipeline from DMI's api
 into a postgres database.
 - 2. A simple API setup to allow others to extract data from the resulting database.

## Description

An in-depth paragraph about your project and overview of use.

## Getting Started

### Dependencies


### postgres_config template:

Filename / path should be

src/configs/postgres_config.py

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

### Executing program

* How to run the program
* Step-by-step bullets
```
code blocks for commands
```

## Help


## Authors


## Version History


## License


## Acknowledgments
