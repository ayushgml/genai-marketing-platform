import psycopg2
from backend.app.config import Config

def create_connection():
    try:
        connection = psycopg2.connect(
            host=Config.RDS_HOST,
            database=Config.RDS_DBNAME,
            user=Config.RDS_USER,
            password=Config.RDS_PASSWORD,
            port=Config.RDS_PORT
        )
        print("Connection to PostgreSQL successful")
        return connection
    except psycopg2.OperationalError as e:
        print(f"The error '{e}' occurred")
        return None

if __name__ == "__main__":
    conn = create_connection()
    if conn:
        conn.close()


# Function to test a query
def execute_test_query(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        result = cursor.fetchone()
        print("PostgreSQL version:", result)
        cursor.close()
    except Exception as e:
        print(f"Failed to execute query: {e}")

if __name__ == "__main__":
    conn = create_connection()
    if conn:
        execute_test_query(conn)
        conn.close()
