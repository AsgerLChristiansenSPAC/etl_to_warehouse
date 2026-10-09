import extract.extract_geojson as geo
import json
from extract import dmi_api


# In case we end up with multiple stations sharing a stationId
def most_recent_station(features):

    id_valid_from = [(feature["id"],feature["properties"]["validFrom"])
                 for feature in features]

    sorted_by_date = sorted(id_valid_from, key=lambda tup: dmi_api.datetime_dmi(tup[1]), reverse=True)

    most_recent_id = sorted_by_date[0][0]

    for feature in features:
        id = feature["id"]
        if id == most_recent_id:
            return feature
    return None


# Todo:

# Implement paging functionality. So, for example, rather than hardcoding the exact amount of data we want to load,
# instead, we can load in a page, transform that and load that, then load in another page...

# Try to define a very narrow datetime range and page through it.

# Basically, it will keep doing nextpage until number returned is zero.

# Such a pager function should take *any* function wrapper for geo.get_query() as an input.



def loop_through_pages(extractor_func):
    # Assumes inner-function returns a feature-collection.
    def inner(*args, batch_limit = 1, **kwargs):
        batch = 0
        feature_collection = extractor_func(*args, **kwargs)
        feature_collections = []
        while batch < batch_limit:
            feature_collections.append(feature_collection)
            links = feature_collection["links"]
            rels = [link["rel"] for link in links]
            if "next" in rels:
                url = links[1]["href"]
                feature_collection = extractor_func(url = url)
                batch += 1
            else:
                print(f"Reached last page before reaching batch limit {batch_limit}")
                break
        # Sometimes, the final feature-collection has no numbers returned.
        if feature_collections[-1]["numberReturned"] == 0:
            feature_collections = feature_collections[:-1]
        return feature_collections
    
    return inner


@loop_through_pages
def get_observations(url:str, **kwargs):
    
    # Decide whether they should overwrite or not.
    query = dmi_api.compose_query(url, parameters=kwargs)
    obs_dict = geo.get_query(query)
    return obs_dict

if __name__ == "__main__":
    import config
    import json
    obs = get_observations(url = config.DEFAULT_URL_OBSERVATION, batch_limit = 50, **config.DEFAULT_PARAMETERS)

    print(len(obs))
    print(json.dumps(obs[-1], indent = 4))
