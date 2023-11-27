from pymongo import MongoClient
import json

def fetchDataFromMongoDB(filter_data):
    print("Fetching data from MongoDB with filter:", filter_data)
    client = MongoClient('mongodb://localhost:27017/') # Replace with your MongoDB URI
    db = client['bf_db'] # Replace with your database name
    collection = db['Properties'] # Replace with your collection name

    # Base query
    query = {}

    # Filtering conditions based on filter_data
    if 'city' in filter_data and filter_data['city']:
        query['city'] = filter_data['city']

    if 'accommodation' in filter_data and filter_data['accommodation']:
        query['accommodation'] = {'$in': filter_data['accommodation']}

    if 'location' in filter_data and filter_data['location']:
        query['sectorNumber'] = {'$in': [location.upper() for location in filter_data['location']]}

    print("MongoDB Query:", query)

    try:
        cursor = collection.find(query)
        results = list(cursor)

        property_links = []

        for item in results:
            if "title" in item and "_id" in item:
                id = str(item['_id'])

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
        print("Failed to fetch data from MongoDB:", e)
        return {"propertyLinks": []}
    finally:
        client.close()

# Example usage
filter_data = {'city': 'GURGAON','accommodation': ['3 BHK'], 'location': ['SUSHANT LOK 1']}
# filter_data = {'city': 'GURGAON'}
response = fetchDataFromMongoDB(filter_data)
print("__________________________________________")
print("response: ", response)
