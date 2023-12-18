import os
from dotenv import load_dotenv
from pdf_reader import LLMDocProccessor

def chat_roulette():
    user_input = ""
    proccessor = LLMDocProccessor(["rafael_pombo.pdf"])
    while user_input != "exit":
        user_input = input("your message (type 'exit' to close): ")
        answer = proccessor.generate_answer(user_input)
        print(answer)

def app():
    load_dotenv()
    if os.getenv("OPENAI_API_KEY") in [None, ""]:
        print("OPENAI_API_KEY not found")
        exit(1)
    chat_roulette()

if __name__ == "__main__":
    app()
