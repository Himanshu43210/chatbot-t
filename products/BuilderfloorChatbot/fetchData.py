
import sqlite3
import json

def fetchDataFromDatabase(filter_data):
    print("Fetching data from database with filter:", filter_data)
    db_path = 'real_estate.db'

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Base query
    query = "SELECT * FROM properties WHERE 1=1"
    parameters = []

    # Filtering conditions based on filter_data
    if 'city' in filter_data and filter_data['city']:
        query += " AND city = ?"
        parameters.append(filter_data['city'])

    if 'accommodation' in filter_data and filter_data['accommodation']:
        # To handle multiple accommodations
        query += " AND accommodation IN ({})".format(', '.join('?'*len(filter_data['accommodation'])))
        parameters.extend(filter_data['accommodation'])

    # if 'location' in filter_data and filter_data['location']:
        

    if 'location' in filter_data and filter_data['location']:
        filter_data['location'] = [location.upper() for location in filter_data['location']]
        # To handle multiple locations
        query += " AND sectorNumber IN ({})".format(', '.join('?'*len(filter_data['location'])))
        parameters.extend(filter_data['location'])

    print("SQL Query:", query)
    print("Parameters:", parameters)

    try:
        cursor.execute(query, parameters)
        rows = cursor.fetchall()

        # Fetch column names from cursor.description
        columns = [description[0] for description in cursor.description]

        # Create a dictionary for each row
        results = [dict(zip(columns, row)) for row in rows]

        property_links = []

        for item in results:
            # Check if necessary keys exist in the item
            if "title" in item and "_id" in item:
                try:
                    # Parse _id as JSON and extract $oid value
                    _id_json = json.loads(item['_id'])
                    id = _id_json.get('$oid', '')
                except json.JSONDecodeError:
                    id = ''  # Handle the case where _id is not a valid JSON string

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

    except sqlite3.Error as e:
        print("Failed to fetch data from the database:", e)
        return {"propertyLinks": []}
    finally:
        conn.close()

# Example usage
filter_data = {'city': 'GURGAON', 'budget': [0, 20000000], 'accommodation': ['3 BHK'], 'location': ['SUSHANT lok 1']}
api_response = fetchDataFromDatabase(filter_data)
print("__________________________________________")
print("api_response: ", api_response)
