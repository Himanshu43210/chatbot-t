
from tinydb import TinyDB, Query
import os
def fetchDataFromDatabase(filter_data):
    print("Fetching data from TinyDB with filter:", filter_data)
    db_path = os.path.join('./products/BuilderfloorChatbot/db.json', 'db.json')
    db = TinyDB(db_path)
    # db = TinyDB('db.json')  
    table = db.table('_default')  
    # TinyDB Query Object
    QueryObj = Query()

    # Base query
    query = []

    # Filtering conditions based on filter_data
    if 'city' in filter_data and filter_data['city']:
        query.append(QueryObj.city == filter_data['city'])

    if 'budget' in filter_data:
        min_budget = int(filter_data['budget'][0]) if filter_data['budget'][0] else 0
        max_budget = int(filter_data['budget'][1]) if len(filter_data['budget']) > 1 else None
        results = table.all()  # Retrieve all records from the table
        filtered_results = []

        for item in results:
            item_price = item.get('price', None)
            if item_price is not None and item_price != "Price on Request":
                try:
                    item_price = int(item_price)  # Convert the price field to an integer
                    if min_budget <= item_price <= max_budget:
                        filtered_results.append(item)
                except ValueError:
                    pass  # Skip items with non-integer price values

    # Floor filter
    if 'floor' in filter_data:
        query.append(QueryObj.floor.one_of(filter_data['floor']))

    # Location filter (uppercase)
    if 'location' in filter_data:
        query.append(QueryObj.sectorNumber.one_of([location.upper() for location in filter_data['location']]))

    # Size filter
    if 'size' in filter_data:
        min_size = filter_data['size'][0] if filter_data['size'][0] else 0
        max_size = filter_data['size'][1] if len(filter_data['size']) > 1 else None
        if max_size:
            query.append((QueryObj.size >= min_size) & (QueryObj.size <= max_size))
        else:
            query.append(QueryObj.size >= min_size)

    # Accommodation filter
    if 'accommodation' in filter_data:
        query.append(QueryObj.accommodation.one_of(filter_data['accommodation']))

    # Possession filter
    if 'possession' in filter_data:
        query.append(QueryObj.possession.one_of(filter_data['possession']))

    # Facing filter
    if 'facing' in filter_data:
        query.append(QueryObj.facing.one_of(filter_data['facing']))

    # Park Facing filter
    if 'parkFacing' in filter_data:
        query.append(QueryObj.parkFacing == filter_data['parkFacing'].upper())

    # Corner filter
    if 'corner' in filter_data:
        query.append(QueryObj.corner == filter_data['corner'].upper())

    print("TinyDB Query:", query)

    try:
        # Combining all query conditions
        final_query = query[0]
        for q in query[1:]:
            final_query &= q

        results = table.search(final_query)

        property_links = []

        for item in results:
            if "title" in item and "_id" in item and "$oid" in item["_id"]:
                custom_id = item["_id"]["$oid"]  # Extracting the custom ID

                formatted_string = (
                    f"https://builderfloor.com/"
                    f"{item['title'].replace(' ', '-').lower()}-"
                    f"{item.get('state', '').replace(' ', '_').upper()}-"
                    f"{item.get('size', '')}SQYD-"
                    f"{item.get('floor', '').replace(' ', '_').upper()}-"
                    f"{item.get('accommodation', '').replace(' ', '_')}-"
                    f"{item.get('facing', '').replace(' ', '_').upper()}-"
                    f"{item.get('possession', '').replace(' ', '_').upper()}-"
                    f"{custom_id}"
                )
                property_links.append(formatted_string)
        return {"propertyLinks": property_links}

    except Exception as e:
        print("Failed to fetch data from TinyDB:", e)
        return {"propertyLinks": []}

# Example usage
# filter_data = {'city': 'GURGAON', 'accommodation': ['3 BHK'], 'location': ['SUSHANT LOK 3']}
filter_data = {'city': 'GURGAON', 'budget': [0, 40000000], 'accommodation': ['3 BHK'], 'location': ['SUSHANT LOK 3']}
response = fetchDataFromDatabase(filter_data)
print("__________________________________________")
print("response: ", response)
