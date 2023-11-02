import os
from dotenv import load_dotenv
from langchain.document_loaders import CSVLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI


def text_to_text_conversation(userQuestion, history, csvLocation, openai_key):
    print("From chatbot: ", openai_key)
    CSV_FILE_PATH = csvLocation + ""
    if userQuestion.lower() == "exit":
        return "Thank You"

    # Setup initial parameters and instances
    loader = CSVLoader(file_path=CSV_FILE_PATH)
    index_creator = VectorstoreIndexCreator()
    docsearch = index_creator.from_loaders([loader])
    print("From chatbot: ", openai_key)
    llm = ChatOpenAI(
        streaming=True,
        temperature=0,
        openai_api_key=openai_key,
    )
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=docsearch.vectorstore.as_retriever(),
        input_key="question",
    )
    initial_statement = "You are a chatbot your main task is to provide proper assistance to the user on whatever is asked by the user. "
    full_query = initial_statement + history

    # Get the answer from langchain
    response = chain({"question": full_query + userQuestion})
    answer = response.get("result", "No answer found.")

    return answer


# Test the method
if __name__ == "__main__":
    chatResponse = text_to_text_conversation(
        "What do you sell and what is my name?",
        "Hi, My name is Isha.",
        "builder_floor.csv",
    )
    print(chatResponse)
