# FetchData.py

import requests


def fetchDataFromApi(filter_data):
    url = "https://bfservices.onrender.com/api/properties/searchPropertiesData"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers, json=filter_data)
        response.raise_for_status()
        data = response.json()

        # Initialize an empty list to hold the formatted strings (property links)
        property_links = []

        # Iterate through the data items
        for item in data.get(
            "data", []
        ):  # Default to empty list if 'data' isn't present
            # Construct the formatted string (property link)
            if "title" in item and "_id" in item:
                # Simplify the replacements and concatenation using f-string
                formatted_string = (
                    f"https://builderfloor.com/"
                    f"{item['title'].replace(' ', '-').lower()}-"
                    f"{item.get('state', '').replace(' ', '_').upper()}-"
                    f"{item.get('size', '')}SQYD-"
                    f"{item.get('floor', '').replace(' ', '_').upper()}-"
                    f"{item.get('accommodation', '').replace(' ', '_')}-"
                    f"{item.get('facing', '').replace(' ', '_').upper()}-"
                    f"{item.get('possession', '').replace(' ', '_').upper()}-"
                    f"{item['_id']}"
                )
                property_links.append(formatted_string)

        # Return a dictionary with the property links
        return {"propertyLinks": property_links}

    except requests.exceptions.RequestException as e:
        print("Failed to connect to the API:", e)
        return {"propertyLinks": []}
