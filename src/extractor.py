import extract.extract_geojson as geo
import json
from extract import dmi_api


def extract_dmi(url:str, **kwargs):
    
    query = dmi_api.compose_query(url, parameters=kwargs)
    obs_dict = geo.get_query(query)
    return obs_dict


if __name__ == "__main__":
    import config
    import json
    extract_dmi_pages = dmi_api.loop_through_pages(extract_dmi)
    obs = extract_dmi_pages(url = config.DEFAULT_URL_OBSERVATION, page_limit = 2, **config.DEFAULT_PARAMETERS)
    # Check how many feature collections
    print(len(obs))
