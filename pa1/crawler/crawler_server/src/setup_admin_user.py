import os
import psycopg2
from werkzeug.security import generate_password_hash

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'db'),
        database=os.getenv('POSTGRES_DB', 'crawler_db'),
        user=os.getenv('POSTGRES_USER', 'crawler_user'),
        password=os.getenv('POSTGRES_PASSWORD', 'crawler_password')
    )
    return conn

def add_admin(username, password):
    password_hash = generate_password_hash(password)
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("INSERT INTO crawldb.crawlers (username, password_hash) VALUES (%s, %s)", (username, password_hash))
                conn.commit()
                print("Admin user added successfully!")
            except psycopg2.IntegrityError:
                print("Username already exists")

if __name__ == "__main__":
    admin_username = "admin"
    admin_password = "secret"
    add_admin(admin_username, admin_password)