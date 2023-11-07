# FetchData.py

import requests


def fetchDataFromApi(filter_data):
    url = "https://bfservices.onrender.com/api/properties/searchPropertiesData"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers, json=filter_data)
        response.raise_for_status()
        data = response.json()

        # Initialize an empty list to hold the formatted strings
        formatted_strings = []

        # Iterate through the data items
        for item in data.get(
            "data", []
        ):  # Use .get to provide a default empty list if 'data' is not present
            # Use the get method with a default value of an empty string for optional keys
            state = item.get("state", "").replace(" ", "_").upper()
            size = f"{item.get('size', '')}SQYD"
            floor = item.get("floor", "").replace(" ", "_").upper()
            accommodation = item.get("accommodation", "").replace(" ", "_")
            facing = item.get("facing", "").replace(" ", "_").upper()
            possession = item.get("possession", "").replace(" ", "_").upper()
            _id = item.get("_id", "")

            # Construct the formatted string only if 'title' and '_id' keys exist
            if "title" in item and "_id" in item:
                title = item["title"].replace(" ", "-").lower()
                formatted_string = f"https://builderfloor.com/{title}-{state}-{size}-{floor}-{accommodation}-{facing}-{possession}-{_id}"
                formatted_strings.append(formatted_string)
            else:
                print("Missing 'title' or '_id' in data item:", item)

        return formatted_strings
    except requests.exceptions.RequestException as e:
        print("Failed to connect to the API:", e)
        return None
