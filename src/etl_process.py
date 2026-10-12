import psycopg
import sys

import config
from etl import extractor, loader, transformer, etl_config
from etl.extract import geojson as e_geo


# Defining extractor functions:

# Defining extract_dmi() as dmi-specific version of geo.get_query()




MOCK_FEATURE_COLLECTION =extractor.extract_dmi_collection(url = etl_config.DEFAULT_URL_STATION,  **etl_config.DEFAULT_STATION_PARAMETERS)


MOCK_FEATURE =e_geo.extract_features(MOCK_FEATURE_COLLECTION
     )[0]

stationParams = transformer.get_dmi_station_parameters(MOCK_FEATURE)

# Here you want to change your database, username & password according to your own values
param_dic = {
    "host"      : config.host_name,
    "dbname"  : config.new_database_name,
    "user"      : config.role_name,
    "password"  : config.role_password.strip("'")
}

table_name = "stationParameters"


cols = stationParams[0]
rows = stationParams[1:]



conn = loader.connect(param_dic)
    # Run the execute_many strategy
loader.insert_rows(conn, cols = cols, rows = rows, table = "stationParameters")
    # Close the connection
conn.close()
