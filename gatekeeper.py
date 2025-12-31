from flask import Flask, request
import requests

app = Flask(__name__)

PROXY_URL = "http://172.31.0.60/query"
FORBIDDEN_KEYWORDS = ["drop", "delete", "truncate", "alter"]

@app.route("/query", methods=["POST"])
def gatekeeper():
    if not request.is_json:
        return "Invalid format", 400

    data = request.get_json(force=True)
    query = data.get("query", "")

    if not query:
        return "Empty query", 400

    if len(query) > 500:
        return "Query too long", 400

    q_lower = query.lower()
    for word in FORBIDDEN_KEYWORDS:
        if word in q_lower:
            return "Forbidden query", 403

    try:
        response = requests.post(
            PROXY_URL,
            json={"query": query},
            timeout=5
        )
        return response.text, response.status_code
    except Exception as e:
        return f"Proxy error: {str(e)}", 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)