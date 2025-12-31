from flask import Flask, request, jsonify
import mysql.connector
import time

app = Flask(__name__)

MANAGER_HOST = "172.31.3.108"
WORKERS = ["172.31.8.205", "172.31.13.137"]

MYSQL_USER = "bench"
MYSQL_PASSWORD = "StrongPassword123!"
MYSQL_DB = "sakila"

def execute_query(query):
    is_write = query.strip().lower().startswith(("insert", "update", "delete"))

    host = MANAGER_HOST if is_write else WORKERS[int(time.time()) % len(WORKERS)]

    try:
        conn = mysql.connector.connect(
            host=host,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            connection_timeout=3
        )

        cursor = conn.cursor()
        cursor.execute(query)

        if is_write:
            conn.commit()
            result = "WRITE OK"
        else:
            result = cursor.fetchall()

        cursor.close()
        conn.close()
        return {"status": "ok", "result": result}

    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()