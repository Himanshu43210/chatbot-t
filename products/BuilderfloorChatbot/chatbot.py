import os
from dotenv import load_dotenv
import openai


def text_to_text_conversation(userQuestion, history):
    os.environ["OPENAI_API_KEY"] = openai_key
    if userQuestion.lower() == "exit":
        return "Thank You"

    # Setup initial parameters
    model = "gpt-3.5-turbo"
    prompt = f""" Create a filter in this format: 
    { 
        "city": "City which is being searched from the query by default it is Gurgaon" ,
        "budget": "Array which contain minimum and maximum budget in number. minimum should be 0 unles and untill query does't specify the minimum ammount",
        "floor": "Array Contain one or more than one Floor options for the Property example 1ST FLOOR ,2ND FLOOR etc",
        "location": "Array Contain one or more than one locations options for the property example Sushant Lok 1, Sushant Lok 2" ,
        "size": "Array contain size of the builder floor minumum and maximum size in number",
        "accommodation": "Array Contain one or more than one accommodation options for the property example 2 BHK, 3 BHK",
        "possession": "Array Contain one or more than one possession options for the property example Ready, 12M (where M denote months)",
        "facing": "Array Contain one or more than one facing options for the property example East, West",
        "sortBy": "When user has specified any sorting of the propertys available, by default it is Price High to Low",
        "parkFacing": "If the property is park facing or not, either YES or NO",
        "corner": "If the property is corner facing or not, either YES or NO"
    }
    if any filter is not applicable, remove it from json. show only the output json.User Query History: {history} and User Query: {userQuestion}"""

    max_tokens = 150  # Adjust as necessary

    # Call to OpenAI API
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=0.5,  # A neutral temperature, adjust as needed
        max_tokens=max_tokens,
    )

    # Get the answer from OpenAI
    answer = response.get("choices", [{}])[0].get("text", "No answer found.").strip()

    return answer


# Test the method
if __name__ == "__main__":
    chatResponse = text_to_text_conversation(
        "What do you sell and what is my name?",
        "Hi, My name is Isha. ",
        "your-openai-api-key",  # Replace with your actual OpenAI API key
    )
    print(chatResponse)
