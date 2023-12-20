from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from llm_answer import LLMDocProccessor


app = Flask(__name__)
CORS(app)

load_dotenv()
chatbot = LLMDocProccessor()


@app.route("/question", methods=["POST"])
def question():
    body = request.json
    if not chatbot.ready:
        return {"statusCode": 404, "body": "Knowledge base not found :("}
        # Verifica si los datos están en formato JSON

    conversation = chatbot.get_conversation_chain()
    answer = conversation({"question": body["data"]})
    print(answer)
    return {"body": answer["answer"]}


if __name__ == "__main__":
    app.run(debug=True)

