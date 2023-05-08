import os
from flask import Flask, request
from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(".env")

app = Flask(__name__)

# Set up the Slack API client
slack_token = os.environ["SLACK_API_TOKEN"]  # Use your bot user's access token
slack_client = WebClient(token=slack_token)

# Set up the Slack signature verifier
slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]  # Use your app's signing secret
signature_verifier = SignatureVerifier(slack_signing_secret)

# Set up the GitHub API credentials
github_token = os.environ["GITHUB_API_TOKEN"]  # Use your GitHub API token

# Define the repositories and their caretakers
repositories = [
    {"name": "TC-api-docs", "link": "https://github.com/tutorcruncher/tc-api-docs", "caretaker": "Seb"},
    {"name": "Socket-frontend", "link": "https://github.com/tutorcruncher/socket-frontend", "caretaker": "Seb"},
    {"name": "Socket-server", "link": "https://github.com/tutorcruncher/socket-server", "caretaker": "Seb"},
    {"name": "uk-postcode-api", "link": "https://github.com/tutorcruncher/uk-postcode-api", "caretaker": "Seb"},
    {"name": "TC-imports", "link": "https://github.com/tutorcruncher/tc-imports", "caretaker": "Dan"},
    {"name": "TC-Intercom", "link": "https://github.com/tutorcruncher/TCIntercom", "caretaker": "Dan"},
    {"name": "Static-maps", "link": "https://github.com/tutorcruncher/static-maps", "caretaker": "Dan"},
    {"name": "TC-virus-checker", "link": "https://github.com/tutorcruncher/tc-virus-checker", "caretaker": "Dan"},
    {"name": "hermes", "link": "https://github.com/tutorcruncher/hermes", "caretaker": "Henty"},
    {"name": "Morpheus", "link": "https://github.com/tutorcruncher/morpheus", "caretaker": "Henty"},
]

# Slash command endpoint for /repos
@app.route("/slack/events", methods=["POST"])
def handle_slash_command():
    # Verify the request signature
    request_body = request.get_data(as_text=True)
    timestamp = request.headers.get("X-Slack-Request-Timestamp")
    signature = request.headers.get("X-Slack-Signature")
    if not signature_verifier.is_valid_request(request_body, timestamp, signature):
        return "", 403

    # Parse the request payload
    payload = request.form.to_dict()
    command = payload.get("command")
    text = payload.get("text")

    if command == "/repos":
        if text == "":
            # Fetch open pull requests and last release for each repository
            for repo in repositories:
                repo_name = repo["name"]
                repo_link = repo["link"]
                caretaker = repo["caretaker"]

                # Fetch open pull requests from GitHub API
                pull_requests_url = f"https://api.github.com/repos/{repo_name}/pulls?state=open"
                headers = {"Authorization": f"Bearer {github_token}"}
                pull_requests_response = requests.get(pull_requests_url, headers=headers)
                pull_requests_count = len(pull_requests_response.json())

                # Fetch last release information
                releases_url = f"https://api.github.com/repos/{repo_name}/releases"
                releases_response = requests.get(releases_url, headers=headers)
                releases = releases_response.json()
                if releases:
                    last_release = releases[0]
                    last_release_date = last_release["published_at"][:10]
                else:
                    last_release_date = "No releases found"

                # Format the message
                message = f"*Repository: {repo_name}*\n" \
                          f"Link: {repo_link}\n" \
                          f"Caretaker: {caretaker}\n" \
                          f"Open Pull Requests: {pull_requests_count}\n" \
                          f"Last Release Date: {last_release_date}"

                # Send the message to the channel
                slack_client.chat_postMessage(channel="#your-channel-name", text=message)

            return "Fetching repository information..."
            else:
            return "Invalid command. Please use `/repos` without any arguments."
    else:
        return "Invalid command. Please use `/repos`."

    if __name__ == "__main__":
        app.run()

