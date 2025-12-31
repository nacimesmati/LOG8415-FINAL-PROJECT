import requests
import time

GATEKEEPER_URL = "http://3.139.81.31/query"

TOTAL_WRITES = 1000
TOTAL_READS = 1000

def send(query):
    r = requests.post(
        GATEKEEPER_URL,
        json={"query": query},
        timeout=5
    )
    return r.status_code, r.text

start = time.time()

print("=== WRITE PHASE ===")
for i in range(TOTAL_WRITES):
    send("INSERT INTO actor (first_name,last_name) VALUES ('Bench','Test')")

print("=== READ PHASE ===")
for i in range(TOTAL_READS):
    send("SELECT COUNT(*) FROM sakila.actor")

end = time.time()

print("DONE")
print(f"Total time: {end-start:.2f}s")


