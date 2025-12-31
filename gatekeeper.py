# Import Flask to create the web service and request to read incoming HTTP data
from flask import Flask, request

# Import requests to forward queries to the Proxy service
import requests

# Create the Flask application
app = Flask(__name__)

# URL of the Proxy service that will execute validated queries
PROXY_URL = "http://172.31.0.60/query"

# List of SQL keywords that are forbidden for security reasons
FORBIDDEN_KEYWORDS = ["drop", "delete", "truncate", "alter"]

# Define the endpoint that clients will use to send SQL queries
@app.route("/query", methods=["POST"])
def gatekeeper():
    # Ensure the request body is in JSON format
    if not request.is_json:
        return "Invalid format", 400

    # Parse the JSON body
    data = request.get_json(force=True)

    # Extract the SQL query from the request
    query = data.get("query", "")

    # Reject empty queries
    if not query:
        return "Empty query", 400

    # Reject excessively long queries
    if len(query) > 500:
        return "Query too long", 400

    # Convert query to lowercase for keyword inspection
    q_lower = query.lower()

    # Block forbidden SQL operations
    for word in FORBIDDEN_KEYWORDS:
        if word in q_lower:
            return "Forbidden query", 403

    try:
        # Forward the validated query to the Proxy service
        response = requests.post(
            PROXY_URL,
            json={"query": query},
            timeout=5
        )

        # Return the Proxy response directly to the client
        return response.text, response.status_code

    except Exception as e:
        # Handle Proxy connection or timeout errors
        return f"Proxy error: {str(e)}", 502


# Start the Gatekeeper service
if __name__ == "__main__":
    # Listen on all interfaces on port 80 (HTTP)
    app.run(host="0.0.0.0", port=80, debug=True)
