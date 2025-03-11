from flask import Flask, jsonify, request
import os
import psycopg2
import threading

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

# Thread lock
lock = threading.Lock()

@app.route('/', methods=['GET'])
def index():
    a = get_db_connection()
    if a:
        print(a)
        return jsonify({"success": True, "message": "Welcome to the Flask app connected to PostgreSQL!"})
    else:
        return jsonify({"success": False, "message": "Failed to connect to PostgreSQL!"})

@app.route('/test', methods=['GET'])
def test():
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT code FROM crawldb.data_type")
    retValue = []
    for counter_id in cur.fetchall():
        retValue.append(counter_id)
    return jsonify({"success": True, "message": "Test successful!", "value": retValue})

@app.route('/data_types', methods=['GET'])
def get_data_types():
    with lock:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM crawldb.data_type")
        data_types = cur.fetchall()
        return jsonify(data_types)

@app.route('/page_types', methods=['GET'])
def get_page_types():
    with lock:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM crawldb.page_type")
        page_types = cur.fetchall()
        return jsonify(page_types)

@app.route('/sites', methods=['GET'])
def get_sites():
    with lock:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM crawldb.site")
        sites = cur.fetchall()
        return jsonify(sites)

@app.route('/pages', methods=['GET'])
def get_pages():
    with lock:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM crawldb.page")
        pages = cur.fetchall()
        return jsonify(pages)

@app.route('/page_data', methods=['GET'])
def get_page_data():
    with lock:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM crawldb.page_data")
        page_data = cur.fetchall()
        return jsonify(page_data)

@app.route('/images', methods=['GET'])
def get_images():
    with lock:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM crawldb.image")
        images = cur.fetchall()
        return jsonify(images)

@app.route('/links', methods=['GET'])
def get_links():
    with lock:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM crawldb.link")
        links = cur.fetchall()
        return jsonify(links)

@app.route('/data_types', methods=['POST'])
def insert_data_type():
    data = request.json
    code = data.get('code')
    if not code:
        return jsonify({"success": False, "message": "Missing 'code' field"}), 400
    with lock:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("INSERT INTO crawldb.data_type (code) VALUES (%s)", (code,))
        con.commit()
        return jsonify({"success": True, "message": "Data type inserted successfully!"})

@app.route('/page_types', methods=['POST'])
def insert_page_type():
    data = request.json
    code = data.get('code')
    if not code:
        return jsonify({"success": False, "message": "Missing 'code' field"}), 400
    with lock:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("INSERT INTO crawldb.page_type (code) VALUES (%s)", (code,))
        con.commit()
        return jsonify({"success": True, "message": "Page type inserted successfully!"})

@app.route('/sites', methods=['POST'])
def insert_site():
    data = request.json
    domain = data.get('domain')
    robots_content = data.get('robots_content')
    sitemap_content = data.get('sitemap_content')
    if not domain:
        return jsonify({"success": False, "message": "Missing 'domain' field"}), 400
    with lock:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("INSERT INTO crawldb.site (domain, robots_content, sitemap_content) VALUES (%s, %s, %s)", 
                    (domain, robots_content, sitemap_content))
        con.commit()
        return jsonify({"success": True, "message": "Site inserted successfully!"})

@app.route('/pages', methods=['POST'])
def insert_page():
    data = request.json
    site_id = data.get('site_id')
    page_type_code = data.get('page_type_code')
    url = data.get('url')
    html_content = data.get('html_content')
    http_status_code = data.get('http_status_code')
    accessed_time = data.get('accessed_time')
    if not site_id or not page_type_code or not url:
        return jsonify({"success": False, "message": "Missing 'site_id', 'page_type_code', or 'url' field"}), 400
    with lock:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("INSERT INTO crawldb.page (site_id, page_type_code, url, html_content, http_status_code, accessed_time) VALUES (%s, %s, %s, %s, %s, %s)", 
                    (site_id, page_type_code, url, html_content, http_status_code, accessed_time))
        con.commit()
        return jsonify({"success": True, "message": "Page inserted successfully!"})

@app.route('/page_data', methods=['POST'])
def insert_page_data():
    data = request.json
    page_id = data.get('page_id')
    data_type_code = data.get('data_type_code')
    data_value = data.get('data')
    if not page_id or not data_type_code or not data_value:
        return jsonify({"success": False, "message": "Missing 'page_id', 'data_type_code', or 'data' field"}), 400
    with lock:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("INSERT INTO crawldb.page_data (page_id, data_type_code, data) VALUES (%s, %s, %s)", 
                    (page_id, data_type_code, data_value))
        con.commit()
        return jsonify({"success": True, "message": "Page data inserted successfully!"})

@app.route('/images', methods=['POST'])
def insert_image():
    data = request.json
    page_id = data.get('page_id')
    filename = data.get('filename')
    content_type = data.get('content_type')
    data_value = data.get('data')
    accessed_time = data.get('accessed_time')
    if not page_id or not filename or not content_type or not data_value or not accessed_time:
        return jsonify({"success": False, "message": "Missing 'page_id', 'filename', 'content_type', 'data', or 'accessed_time' field"}), 400
    with lock:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("INSERT INTO crawldb.image (page_id, filename, content_type, data, accessed_time) VALUES (%s, %s, %s, %s, %s)", 
                    (page_id, filename, content_type, data_value, accessed_time))
        con.commit()
        return jsonify({"success": True, "message": "Image inserted successfully!"})

@app.route('/links', methods=['POST'])
def insert_link():
    data = request.json
    from_page = data.get('from_page')
    to_page = data.get('to_page')
    if not from_page or not to_page:
        return jsonify({"success": False, "message": "Missing 'from_page' or 'to_page' field"}), 400
    with lock:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("INSERT INTO crawldb.link (from_page, to_page) VALUES (%s, %s)", 
                    (from_page, to_page))
        con.commit()
        return jsonify({"success": True, "message": "Link inserted successfully!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)