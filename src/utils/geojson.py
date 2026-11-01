import copy

# Functions currently in use in the code.

def get_property(feature:dict, property:str):
    """A geojson 'feature' object has a 'properties' member, which itself
    contains json key-value pairs - a property name, and a value.
    This function extracts the value of a specific property from
    a geojson feature object."""
    
    return feature["properties"][property]



def get_features(feature_collection:dict):
    """A featureCollection geojson object is a dictionary containing
    feature objects, plus some additional information about the query
    which produced the featureColleciton.
    The feature objects themselves are the most
    important member of a featureCollection.
    This function extracts them."""
    try:
        features = feature_collection["features"] # List of dicts.
        return features
    except KeyError as e:
        print(e)
        print("No features found, maybe not feature-collection")
        return None


# Functions intended for handling geojson properties whose values are JSON arrays,
# rather than floats, strings, etc.
# An example from the DMI API climate data is the parameterId variable,
# which maps the relation between a weather station and the many
# different types of parameters it estimates.
# As such, a geojson feature of type "station" has many
# parameterId's, whereas a feature of type "observation"
# only has one.
# The functions below were intended to make it possible
# to dynamically handle geojson properties which are arrays.

# Status: Unfinished. Which is to say, the functions work, but their exact
# implementation (such as when the relevant properties are extracted from
# the geojson features) are currently at odds with transformer.py



def get_property_dict(feature:dict, property:str):
    return {property : get_property(feature, property)}

def get_many_properties(feature:dict, properties:list):
    """This function extracts particularly relevant properties,
    specified by input 'properties', from a feature object,
    and returns a dictionary of property-value pairs.
    Such dicts are very useful for inserting data
    in an SQL table."""
    property_dict = {}
    for property in properties:
        new_property_dict = get_property_dict(feature, property)
        # Add key-value pair to dict.
        property_dict.update(new_property_dict)
    return property_dict


def append_category_value(property_dict, category_property, category_value):
    """Appends a category value to an existing dict without one -
    i.e. appending a new column and corresponding value
    to an existing row."""
    category_dict = {category_property : category_value}
    # Create a DEEP COPY of properties dictionary.
    combination = copy.deepcopy(property_dict)
    # Add category
    combination.update(category_dict)
    return combination

def combine_with_category(property_dict, category_property, category_values):
    category_idx = list(range(0,len(category_values)))
    combinations = [
    append_category_value(property_dict,
                                category_property,
                                category_values[idx])
                                for idx in category_idx]
    return combinations


def extend_combinations(category_property, category_values, combinations:list):
    new_combinations = []
    for combination in combinations: # combination is a dict
        new_combination = combine_with_category(
            property_dict = combination,
            category_property=category_property
            ,
            category_values=category_values)
        new_combinations.extend(new_combination)
    return new_combinations


def combine_many_categories(feature, property_dict, category_properties):
    combinations = []
    for category_property in category_properties:        
        category_values = get_property(feature, category_property)
        if len(combinations) == 0:
            combinations = combine_with_category(property_dict, category_property, category_values)
        else:
            combinations = extend_combinations(category_property, category_values,combinations,)
    return combinations

def combine_all_categories(feature, properties, category_properties:list):
    property_dict = get_many_properties(feature, properties)
    if len(category_properties) > 1:
        return combine_many_categories(feature, property_dict, category_properties)
    elif len(category_properties) == 1:
        category_property = category_properties[0]
        category_values = get_property(feature, category_property)
        return combine_with_category(property_dict, category_property, category_values)


if __name__ == "__main__":
    import json
    MOCK_FEATURE = {
        "properties" : {
            "a" : 1,
            "b" : 2,
            "c" : 3,
            "d" : "monkey",
            "e" : "highly irrelevant",
            "a_id" : ["1","2","3","4"],
            "b_id" : [333,444,555,666],
            "c_id" : ["alpha", "beta", "gamma"],
            "d_id" : ["red", "blue", "green"]
        }
    }

    tests = [
    {
    "relevant_properties" : ["a", "b"],
    "relevant_categories" : ["a_id"] # Should result in 4 rows
    ,
    "length" : 4
    }
    ,
    {
    "relevant_properties" : ["a", "b"],
    "relevant_categories" : ["a_id", "b_id"]
    ,
    "length" : 16

    }
    ,{
    "relevant_properties" : ["a", "b"],
    "relevant_categories" : ["a_id", "b_id","c_id"]
    ,
    "length" : 48
    }
    ,
    {
    "relevant_properties" : ["a", "b"],
    "relevant_categories" : ["a_id", "b_id","c_id", "d_id"]
    ,
    "length" : 48*3
    }
    ]
    for test in tests:
        relevant_properties = test["relevant_properties"]
        relevant_categories = test["relevant_categories"]
        combi = combine_all_categories(feature = MOCK_FEATURE,
                                       properties = relevant_properties,
                                       category_properties=relevant_categories)
#       print(json.dumps(combi, indent=4))
        try:
            assert test["length"] == len(combi)
        except AssertionError:
            print("Error!")
            print(f'Should be {test["length"]}, is actually {len(combi)}')
#    print(combi)
