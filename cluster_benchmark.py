# Import requests to send HTTP requests to the Gatekeeper service
import requests

# Import time to measure total execution duration
import time

# URL of the Gatekeeper endpoint that receives SQL queries
GATEKEEPER_URL = "http://3.139.81.31/query"

# Number of write operations to execute
TOTAL_WRITES = 1000

# Number of read operations to execute
TOTAL_READS = 1000

# Helper function to send a SQL query to the Gatekeeper
def send(query):
    # Send the SQL query as JSON in a POST request
    r = requests.post(
        GATEKEEPER_URL,
        json={"query": query},
        timeout=5
    )
    # Return the HTTP status code and response body
    return r.status_code, r.text

# Record the start time of the benchmark
start = time.time()

# Write phase: insert rows into the database through the Gatekeeper
print("=== WRITE PHASE ===")
for i in range(TOTAL_WRITES):
    send("INSERT INTO actor (first_name,last_name) VALUES ('Bench','Test')")

# Read phase: execute read queries through the Gatekeeper
print("=== READ PHASE ===")
for i in range(TOTAL_READS):
    send("SELECT COUNT(*) FROM sakila.actor")

# Record the end time of the benchmark
end = time.time()

# Print benchmark completion and total execution time
print("DONE")
print(f"Total time: {end-start:.2f}s")
