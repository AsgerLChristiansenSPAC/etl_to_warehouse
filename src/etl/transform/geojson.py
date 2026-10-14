import copy

def get_property(feature:dict, property:str):
    return feature["properties"][property]

def organize_properties(feature:dict, properties:list):
    """Assumes NO ARRAY PROPERTY in properties!"""
    property_dict = {}
    for property in properties:
        value = get_property(property)
        # Add key-value pair to dict.
        property_dict.update({property : value})
    return property_dict

def organize_array_property(feature:dict, array_property:str):
    """Gets an array property from feature object,
    and returns dictionary containing a single list."""
    name = array_property
    category_list = get_property(feature, array_property)
    return {name : category_list}

def combine_properties(properties, array_property):
    pass
#    dict_1 = organize_properties(properties)
#    dict_2 = organize_array_property(array_property)
#    combinations = []
#    n = len(dict_2[array_property])
#    for i in list(range(0,n)):
#        combination = copy.deepcopy(dict_1)
#        combination.update({array_property, dict_2[array_property]})
#        combinations.append(combination)




def get_features(feature_collection:dict):
    try:
        features = feature_collection["features"] # List of dicts.
        return features
    except KeyError as e:
        print(e)
        print("No features found, maybe not feature-collection")
        return None