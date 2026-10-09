# Transform functions specific to DMI's climate API.
import datetime

def datetime_dmi(date_time):
    format = '%Y-%m-%dT%H:%M:%SZ'
    datetime_str = datetime.datetime.strptime(date_time, format)

    return datetime_str


## If useful to specify parameters as dict, use these functions:

def index_parameter_keys(parameters:dict):
    keys = list(parameters.keys())
    key_indeces = list(range(0,len(keys)))
    indexed_keys = [(keys[idx], idx) for idx in key_indeces]
    return indexed_keys

def chain_parameter(query_tail:str, key:str, value:str, first = False):
    key_val = key + '=' + value
    if first:
        query_tail = query_tail + key_val
    else:
        query_tail = query_tail + '&' + key_val
    return query_tail
    

def chain_parameters(parameters:dict):
    indexed_keys = index_parameter_keys(parameters)
    query_tail = '?'
    for key, idx in indexed_keys:
        value = str(parameters[key])
        if idx == 0: # If first entry, no ampersand
            query_tail = chain_parameter(query_tail, key, value, first = True)
        else: # If not first entry
            query_tail = chain_parameter(query_tail, key, value)
    return query_tail


def compose_query(url, parameters:dict = {}):
    if len(parameters)>0:
        query_tail = chain_parameters(parameters)
        query = url + query_tail
    else:
        query = url
    return query
        



def most_recent_station(features):

    id_valid_from = [(feature["id"],feature["properties"]["validFrom"])
                 for feature in features]

    sorted_by_date = sorted(id_valid_from, key=lambda tup: datetime_dmi(tup[1]), reverse=True)

    most_recent_id = sorted_by_date[0][0]

    for feature in features:
        id = feature["id"]
        if id == most_recent_id:
            return feature
    return None


def loop_through_pages(extractor_func):
    # Assumes inner-function returns a feature-collection.
    def inner(*args, page_limit = 1, **kwargs):
        page = 0
        feature_collection = extractor_func(*args, **kwargs)
        feature_collections = []
        while page < page_limit:
            feature_collections.append(feature_collection)
            links = feature_collection["links"]
            rels = [link["rel"] for link in links]
            if "next" in rels:
                url = links[1]["href"]
                feature_collection = extractor_func(url = url)
                page += 1
            else:
                print(f"Reached last page before reaching page limit {page_limit}")
                break
        # Sometimes, the final feature-collection has no numbers returned.
        if feature_collections[-1]["numberReturned"] == 0:
            feature_collections = feature_collections[:-1]
        return feature_collections
    
    return inner