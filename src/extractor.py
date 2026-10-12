import extract.extract_geojson as geo
import json
from extract import dmi_api

# Defining extract_dmi() as dmi-specific version of geo.get_query()

extract_dmi = dmi_api.dmi_query(geo.get_query)

# Make the function able to loop through pages.
extract_dmi_pages = dmi_api.loop_through_pages(extract_dmi)


if __name__ == "__main__":
    import config
    import json
    obs = extract_dmi_pages(url = config.DEFAULT_URL_OBSERVATION, page_limit = 2, **config.DEFAULT_PARAMETERS)
    # Check how many feature collections
    print(len(obs))
