# Import Flask to create the API, request to read incoming data, and jsonify for JSON responses
from flask import Flask, request, jsonify

# Import MySQL connector to communicate with MySQL databases
import mysql.connector

# Import time to implement simple load distribution
import time

# Create the Flask application
app = Flask(__name__)

# IP address of the MySQL manager node (handles all writes)
MANAGER_HOST = "172.31.3.108"

# IP addresses of MySQL worker nodes (handle read queries)
WORKERS = ["172.31.8.205", "172.31.13.137"]

# MySQL authentication credentials
MYSQL_USER = "bench"
MYSQL_PASSWORD = "StrongPassword123!"
MYSQL_DB = "sakila"

# Function responsible for executing SQL queries on the appropriate node
def execute_query(query):
    # Determine if the query is a write operation
    is_write = query.strip().lower().startswith(("insert", "update", "delete"))

    # Select manager for writes, worker for reads (simple time-based round-robin)
    host = MANAGER_HOST if is_write else WORKERS[int(time.time()) % len(WORKERS)]

    try:
        # Establish a connection to the selected MySQL node
        conn = mysql.connector.connect(
            host=host,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            connection_timeout=3
        )

        # Create a cursor to execute SQL statements
        cursor = conn.cursor()

        # Execute the SQL query
        cursor.execute(query)

        if is_write:
            # Commit changes for write operations
            conn.commit()
            result = "WRITE OK"
        else:
            # Fetch results for read operations
            result = cursor.fetchall()

        # Close cursor and database connection
        cursor.close()
        conn.close()

        # Return successful execution result
        return {"status": "ok", "result": result}

    except Exception as e:
        # Handle database connection or execution errors
        return {"status": "error", "error": str(e)}

# Define the Proxy endpoint that receives queries from the Gatekeeper
@app.route("/query", methods=["POST"])
def query():
    # Parse the JSON body sent by the Gatekeeper
    data = request.get_json()
