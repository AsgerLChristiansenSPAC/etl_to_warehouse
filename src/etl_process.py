import psycopg
import sys

import config
from etl import extractor, loader, transformer, etl_config
from etl import transform


# Defining extractor functions:


# Here you want to change your database, username & password according to your own values

def etl(host, dbname, user, url, table, **kwargs):
    # kwargs specify query parameters
    # if DMI:

    # EXTRACT:
    featureCollection =extractor.extract_dmi_collection(url = url,  **kwargs)
    
    
    # TRANSFORM:
    features = transform.geojson.get_features(featureCollection)
    for feature in features:
        if table == "stationParameters":
            stationParams = transformer.get_dmi_station_parameters(feature)

            # LOAD TO DB
            loader.load(host, dbname, user, table, data = stationParams)

if __name__ == "__main__":
    TEST_INFO = {
    "host"      : config.host_name,
    "dbname"  : config.new_database_name,
    "user"      : config.role_name,
    "url" : etl_config.DEFAULT_URL_STATION,
    "table" : "stationParameters",
    }

    etl(**TEST_INFO, **etl_config.DEFAULT_STATION_PARAMETERS)

