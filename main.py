import os
import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

api_url = "https://sidekick-server-ezml2kwdva-uc.a.run.app/ask_llm"
bearer_token = "8cbbdd2e-c110-47f5-b47d-5a7e4e105b10"
headers = {"Authorization": f"Bearer {bearer_token}", "Content-Type": "application/json"}


def get_answer(question):
    data = {
        "queries": [
            {
                "query": question,
                "filter": {"source_type": "web"},
                "top_k": 3,
            }
        ],
        "possible_intents": [
            {"name": "question", "description": "user is asking a question"}
        ],
    }
    response = requests.post(api_url, headers=headers, json=data)
    response_json = response.json()
    answer = response_json["results"][0]["answer"]
    return answer


app = App(token=os.environ["SLACK_BOT_TOKEN"])

@app.event("message")
def handle_message(event, say):
    question = event["text"]
    answer = get_answer(question)
    say(answer)


if __name__ == "__main__":
    handler = SocketModeHandler(app_token=os.environ["SLACK_APP_TOKEN"])
    handler.start()
