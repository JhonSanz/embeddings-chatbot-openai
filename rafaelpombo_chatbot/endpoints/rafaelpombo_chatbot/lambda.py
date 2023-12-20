import json
from llm_answer import LLMDocProccessor


def lambda_handler(event, context):
    body = json.loads(event["body"])
    if not body.get("question"):
        return {"statusCode": 400, "body": "Bad body bro"}

    chatbot = LLMDocProccessor()
    if not chatbot.ready:
        return {"statusCode": 404, "body": "Knowledge base not found :("}
    conversation = chatbot.get_conversation_chain()
    answer = conversation({"question": body["question"]})
    return {"statusCode": 200, "body": json.dumps({"answer": answer})}
