import json
import os
import openai
from dotenv import load_dotenv

# from fetchData1 import fetchDataFromApi
from fetchData import fetchDataFromDatabase

# Load the environment variables from .env file
load_dotenv()


def text_to_text_conversation(userQuestion, history):
    # Retrieve the OpenAI API key from environment variables
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key is None:
        raise ValueError("The OPENAI_API_KEY is not set in the environment.")

    if userQuestion.lower() == "exit":
        return "Thank You"

    # Setup initial parameters for chat
    model = "gpt-3.5-turbo"

    # Format the prompt as a conversation, if necessary
    conversation = [
        {
            "role": "system",
            "content": """Hi, If I ask you question regarding any property/builderfloor etc, then create a filter in this format and set isFilter property  as 'True' and if I ask you general questions and filters are not being generated, then set isFilter perperty as 'False' then do not create filter : 
            {{
                "data": "Answer to normal query and general question answers"
                "isFilter":true,
                "filterData": {{ 
                    "city": "City which is being searched from the query by default it is GURGAON and it is case sensitive, it should always be in upper case.",
                    "budget": "Array which contain minimum and maximum budget in number. minimum should be 0 unless and until query doesn't specify the minimum amount",
                    "floor": "Array Contain one or more than one Floor options for the Property example 1ST FLOOR, 2ND FLOOR etc",
                    "location": "Array Contain one or more than one locations options for the property example Sushant Lok 1, Sushant Lok 2, Sector 27, change it to upper case.",
                    "size": "Array contain size of the builder floor minimum and maximum size in number",
                    "accommodation": "Array Contain one or more than one accommodation options for the property example 2 BHK, 3 BHK",
                    "possession": "Array Contain one or more than one possession options for the property example Ready, 12M (where M denote months)",
                    "facing": "Array Contain one or more than one facing options for the property example East, West",
                    "sortBy": "When user has specified any sorting of the properties available, by default it is Price High to Low",
                    "parkFacing": "If the property is park facing or not, either YES or NO",
                    "corner": "If the property is corner facing or not, either YES or NO"
                    }}
            }}
            If any filter is not applicable, remove it from json. Show only the output json.""",
        },
        {"role": "user", "content": history},
        {"role": "user", "content": userQuestion},
    ]

    # Call to OpenAI chat API
    response = openai.ChatCompletion.create(
        model=model,
        messages=conversation,
        api_key=openai_api_key,  # Use the API key from the environment variable
    )

    # Get the answer from OpenAI
    answer = (
        response.get("choices", [{}])[0]
        .get("message", {})
        .get("content", "No answer found.")
        .strip()
    )
    print("Received answer from OpenAI:", answer)

    final_response = None
    filter_data = {} 
    # Convert the string answer to a JSON object if it is JSON-formatted
    try:
        # Remove any unwanted newlines and backslashes from the string
        answer = answer.replace("\n", "").replace("\\", "")
        # Attempt to convert the string to a JSON object
        answer_json = json.loads(answer)
        print('answer_json: ', answer_json)

        print(answer)
        if isinstance(answer_json, dict) and answer_json.get("isFilter"):
            print("step 1")
            # Directly access 'filterData' from answer_json, not from answer_json["data"]
            filter_data = answer_json.get("filterData", {})
            # filter_data = answer_json["filterData"]
            # filter_data = answer_json["data"]["filterData"]
            print("step 2")
            # api_response = fetchDataFromApi(filter_data)
            api_response = fetchDataFromDatabase(filter_data)
            print("api_response: ", api_response)
            print("step 3")
            if api_response and api_response.get('propertyLinks') == []:
                final_response = {
                    "data": "Sorry, no match found for your query",
                    "isFilter": True,
                    "filterData": filter_data,
                    "propertyLinks": ""
                }
            elif api_response == 'Not found':
                final_response = {
                    "data": "Sorry, no match found for your query",
                    "isFilter": True,
                    "filterData": filter_data,
                    "propertyLinks": ""
                }
            elif api_response:
                final_response = {
                    "data": answer_json.get("data", "No answer found."),
                    "isFilter": True,
                    "filterData": filter_data,
                    "propertyLinks": api_response["propertyLinks"]
                }
                print(json.dumps(final_response, indent=4))
                
            else:
                print("step 5")
                print("No data received from API.")
           
        else:
            print("Not found")
    except json.JSONDecodeError:
        # If an error occurs, the answer is not JSON-formatted, so return as is
        answer_json = answer
    
    if final_response is None:
        final_response = {
                    "data": "Sorry, no match found for your query",
                    "isFilter": True,
                    "filterData": {},
                    "propertyLinks": ""
                }
    return final_response


# Test the method
if __name__ == "__main__":
    # chatResponse = text_to_text_conversation(
    #     "I am looking for a 3BHK flat in SUSHANT LOK 2 under 4 Crores.", "Hi, My name is Isha."
    # )
    # chatResponse = text_to_text_conversation("I am looking for a 3BHK flat in SECTOR 26 under 4 Crores.", "Hi, My name is Isha.")
    chatResponse = text_to_text_conversation("I am looking for a 3BHK flat in Sushant Lok 3 under 4 crores", "Hi, My name is Isha.")
    print(chatResponse)
