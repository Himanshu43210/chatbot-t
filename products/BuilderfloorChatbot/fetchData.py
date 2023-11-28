# from tinydb import TinyDB

# # Specify the path to the JSON file
# db_path = "products/BuilderfloorChatbot/BF_property_data.json"

# # Initialize a TinyDB instance and open the JSON file
# db = TinyDB(db_path)

# Fetching data from Tiny DB
from tinydb import TinyDB, Query
import json

def fetchDataFromDatabase(filter_data):
    print("Fetching data from TinyDB with filter:", filter_data)
    db = TinyDB('db.json')  # Replace with your TinyDB file path
    collection = db.table('Properties')  # Replace with your table name

    # TinyDB query object
    QueryObj = Query()

    # Base query
    query = []

    # Filtering conditions based on filter_data
    if 'city' in filter_data and filter_data['city']:
        query.append(QueryObj.city == filter_data['city'])

    # Budget filter
    if 'budget' in filter_data:
        min_budget = filter_data['budget'][0] if filter_data['budget'][0] else 0
        max_budget = filter_data['budget'][1] if len(filter_data['budget']) > 1 else None
        if max_budget:
            query.append((QueryObj.budget >= min_budget) & (QueryObj.budget <= max_budget))
        else:
            query.append(QueryObj.budget >= min_budget)

    # Floor filter
    if 'floor' in filter_data:
        query['floor'] = {'$in': filter_data['floor']}

    # Location filter (uppercase)
    if 'location' in filter_data:
        query['sectorNumber'] = {'$in': [location.upper() for location in filter_data['location']]}

    # Size filter
    if 'size' in filter_data:
        min_size = filter_data['size'][0] if filter_data['size'][0] else 0
        max_size = filter_data['size'][1] if len(filter_data['size']) > 1 else None
        if max_size:
            query['size'] = {'$gte': min_size, '$lte': max_size}
        else:
            query['size'] = {'$gte': min_size}

    # Accommodation filter
    if 'accommodation' in filter_data:
        query['accommodation'] = {'$in': filter_data['accommodation']}

    # Possession filter
    if 'possession' in filter_data:
        query['possession'] = {'$in': filter_data['possession']}

    # Facing filter
    if 'facing' in filter_data:
        query['facing'] = {'$in': filter_data['facing']}

    # Park Facing filter
    if 'parkFacing' in filter_data:
        query['parkFacing'] = filter_data['parkFacing'].upper()

    # Corner filter
    if 'corner' in filter_data:
        query['corner'] = filter_data['corner'].upper()

    print("TinyDB Query:", query)

    try:
        if query:
            combined_query = query[0]
            for q in query[1:]:
                combined_query &= q
            results = collection.search(combined_query)
        else:
            results = collection.all()

        property_links = []

        for item in results:
            if "title" in item:
                id = item.doc_id  # TinyDB uses doc_id as the unique identifier

                formatted_string = (
                    f"https://builderfloor.com/"
                    f"{item['title'].replace(' ', '-').lower()}-"
                    f"{item.get('state', '').replace(' ', '_').upper()}-"
                    f"{item.get('size', '')}SQYD-"
                    f"{item.get('floor', '').replace(' ', '_').upper()}-"
                    f"{item.get('accommodation', '').replace(' ', '_')}-"
                    f"{item.get('facing', '').replace(' ', '_').upper()}-"
                    f"{item.get('possession', '').replace(' ', '_').upper()}-"
                    f"{id}"
                )
                property_links.append(formatted_string)
        return {"propertyLinks": property_links}

    except Exception as e:
        print("Failed to fetch data from TinyDB:", e)
        return {"propertyLinks": []}

# Example usage
filter_data = {'city': 'GURGAON', 'accommodation': ['3 BHK'], 'location': ['SUSHANT LOK 3']}
response = fetchDataFromDatabase(filter_data)
print("__________________________________________")
print("response: ", response)
