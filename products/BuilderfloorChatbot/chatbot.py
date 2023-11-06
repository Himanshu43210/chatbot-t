import json
import os
from dotenv import load_dotenv
import openai

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
            "content": """Hi, If I ask you question regarding any property/builderfloor etc, then create a filter in this format and set isFilter property  as true and if I ask you general questions and filters are not being generated, then set isFilter perperty as false then do not create filter : 
            {{
                "data": "Answer to normal query and general question answers"
                "isFilter":true,
                "filterData": {{ 
                    "city": "City which is being searched from the query by default it is Gurgaon",
                    "budget": "Array which contain minimum and maximum budget in number. minimum should be 0 unless and until query doesn't specify the minimum amount",
                    "floor": "Array Contain one or more than one Floor options for the Property example 1ST FLOOR, 2ND FLOOR etc",
                    "location": "Array Contain one or more than one locations options for the property example Sushant Lok 1, Sushant Lok 2",
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

    # Convert the string answer to a JSON object if it is JSON-formatted
    try:
        # Remove any unwanted newlines and backslashes from the string
        answer = answer.replace("\n", "").replace("\\", "")

        # Attempt to convert the string to a JSON object
        answer_json = json.loads(answer)
    except json.JSONDecodeError:
        # If an error occurs, the answer is not JSON-formatted, so return as is
        answer_json = answer

    return answer_json


# Test the method
if __name__ == "__main__":
    chatResponse = text_to_text_conversation(
        "What do you sell and what is my name?", "Hi, My name is Isha."
    )
    print(chatResponse)
