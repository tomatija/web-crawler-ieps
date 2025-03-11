from flask import Flask
from flask import jsonify
import os
import psycopg2

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'db'),
        database=os.getenv('POSTGRES_DB', 'crawler_db'),
        user=os.getenv('POSTGRES_USER', 'crawler_user'),
        password=os.getenv('POSTGRES_PASSWORD', 'crawler_password')
    )
    return conn

@app.route('/', methods=['GET'])
def index():
    a = get_db_connection()
    if a:
        print(a)
        return jsonify({"success":True, "message": "Welcome to the Flask app connected to PostgreSQL!"})
    else:
        return jsonify({"success":False, "message": "Failed to connect to PostgreSQL!"})


@app.route('/test', methods=['GET'])
def test():
    con = get_db_connection()

    cur = con.cursor()
    cur.execute("SELECT code FROM crawldb.data_type")
    retValue  = []
    for counter_id in cur.fetchall():
        retValue.append(counter_id)
    return jsonify({"success":True, "message": "Test successful!", "value": retValue})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)