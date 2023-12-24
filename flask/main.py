import json
from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
from llm_answer import LLMDocProccessor
from local_memory import LocalMemory

app = Flask(__name__)
CORS(app)

load_dotenv()
chatbot = LLMDocProccessor("renacuajo_paseador_faiss_index")


@app.route("/answer", methods=["POST"])
def answer():
    body = request.json
    if not chatbot.ready:
        return {"statusCode": 404, "body": "Knowledge base not found :("}

    conversation = chatbot.get_conversation_chain()
    answer = conversation({"question": body["data"]})
    print(answer)
    return {"body": answer["answer"]}


@app.route("/question", methods=["POST"])
def question():
    body = request.json
    if not chatbot.ready:
        return {"statusCode": 404, "body": "Knowledge base not found :("}

    memory_manager = LocalMemory()
    memory = memory_manager.get_memory()
    prompt = f"Evita preguntarme preguntas similares a estas: {memory}"
    if memory:
        question = f'{body["data"]}. {prompt}'
    else:
        question = f'{body["data"]}'
    conversation = chatbot.get_conversation_chain()
    answer = conversation({"question": question})
    memory_manager.set_memory(answer["answer"])
    print(answer)
    return {"body": answer["answer"]}


if __name__ == "__main__":
    app.run(debug=True)
