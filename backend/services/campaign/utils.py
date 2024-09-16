import logging
import psycopg2
import uuid
from app.config import Config

logger = logging.getLogger(__name__)

def create_table_if_not_exists(conn):
    """Creates the 'campaign_data' table in PostgreSQL if it doesn't already exist."""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS campaign_data (
        client_id VARCHAR(255),
        prod_id VARCHAR(255),
        campaign_id VARCHAR(255) PRIMARY KEY,
        campaign_type VARCHAR(255),
        length INT,
        target_demographic VARCHAR(255)
    );
    """
    try:
        cur = conn.cursor()
        cur.execute(create_table_sql)
        conn.commit()
        print("Table checked/created successfully!")
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        if cur:
            cur.close()

def insert_record_into_rds(record):
    """Inserts a single record into the 'campaign_data' table in PostgreSQL RDS, generating a unique campaign_id."""

    # Generate a unique campaign_id using uuid4
    campaign_id = str(uuid.uuid4())

    # SQL statement to insert a record
    insert_sql = """
    INSERT INTO campaign_data (client_id, prod_id, campaign_id, campaign_type, length, target_demographic)
    VALUES (%s, %s, %s, %s, %s, %s);
    """

    # Values to insert (from the record argument and generated campaign_id)
    values = (
        record['client_id'],
        record['prod_id'],
        campaign_id,  # Use the generated campaign_id
        record['campaign_type'],
        record['length'],
        record['target_demographic']
    )

    conn=None

    # Connect to the PostgreSQL RDS instance
    try:
        # Connection details
        conn = psycopg2.connect(
            host=Config.RDS_HOST,
            database=Config.RDS_DBNAME,
            user=Config.RDS_USER,
            password=Config.RDS_PASSWORD,
            port=Config.RDS_PORT
        )

        # Create table if it doesn't exist
        create_table_if_not_exists(conn)

        # Insert the record
        cur = conn.cursor()
        cur.execute(insert_sql, values)
        conn.commit()
        print(f"Record inserted successfully with campaign_id: {campaign_id}")
    except Exception as e:
        print(f"Error inserting record: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

def insert_record_into_db(record, client_id, product_id):
    """Inserts a single record into the 'campaign_data' table in PostgreSQL RDS, generating a unique campaign_id."""
    print("ram")
    # Generate a unique campaign_id using uuid4
    campaign_id = str(uuid.uuid4())

    # SQL statement to insert a record
    insert_sql = """
    INSERT INTO campaign_data (client_id, prod_id, campaign_id, campaign_type, length, target_demographic)
    VALUES (%s, %s, %s, %s, %s, %s);
    """

    # Values to insert (from the record argument and generated campaign_id)
    values = (
        client_id,
        product_id,
        campaign_id,  # Use the generated campaign_id
        record['campaign_type'],
        record['length'],
        record['target_demographic']
    )

    # Connect to the PostgreSQL RDS instance
    try:
        # Connection details
        conn = psycopg2.connect(
            host=Config.RDS_HOST,
            database=Config.RDS_DBNAME,
            user=Config.RDS_USER,
            password=Config.RDS_PASSWORD,
            port=Config.RDS_PORT
        )

        # Create table if it doesn't exist
        create_table_if_not_exists(conn)

        # Insert the record
        cur = conn.cursor()
        cur.execute(insert_sql, values)
        conn.commit()
        print(f"Record inserted successfully with campaign_id: {campaign_id}")
        return campaign_id
    except Exception as e:
        print(f"Error inserting record: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

def get_campaign_from_client(client_id, product_id):
    """Retrieves a campaign record from the 'campaign_data' table in PostgreSQL RDS based on client_id and product_id."""

    select_sql = """
    SELECT * FROM campaign_data
    WHERE client_id = %s
    AND prod_id = %s;
    """

    conn = None

    try:
        # Connection details
        conn = psycopg2.connect(
            host=Config.RDS_HOST,
            database=Config.RDS_DBNAME,
            user=Config.RDS_USER,
            password=Config.RDS_PASSWORD,
            port=Config.RDS_PORT
        )

        # Execute the SELECT query
        cur = conn.cursor()
        cur.execute(select_sql, (client_id, product_id))

        # Fetch the result
        result = cur.fetchone()

        if result:
            result_json = {
                "client_id": result[0],
                "prod_id": result[1],
                "campaign_id": result[2],
                "campaign_type": result[3],
                "length": result[4],
                "target_demographic": result[5]
            }
            return result_json
        else:
            logger.error("Campaign record not found.")
            return None

    except Exception as e:
        logger.error(f"Error retrieving campaign record: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()
def get_campaign_from_client_only(client_id):
    """Retrieves a campaign record from the 'campaign_data' table in PostgreSQL RDS based on client_id ."""

    select_sql = """
    SELECT * FROM campaign_data
    WHERE client_id = %s
    """
    conn = None

    try:
        # Connection details
        conn = psycopg2.connect(
            host=Config.RDS_HOST,
            database=Config.RDS_DBNAME,
            user=Config.RDS_USER,
            password=Config.RDS_PASSWORD,
            port=Config.RDS_PORT
        )

        # Execute the SELECT query
        cur = conn.cursor()
        cur.execute(select_sql, (client_id,))

        # Fetch the result
        result = cur.fetchall()
        if result:
            result_jsons = []
            for r in result:
                result_jsons.append({
                    "client_id": r[0],
                    "prod_id": r[1],
                    "campaign_id": r[2],
                    "campaign_type": r[3],
                    "length": r[4],
                    "target_demographic": r[5]
                })
            print(result_jsons)
            return result_jsons
        else:
            logger.error("Campaign record not found.")
            return None

    except Exception as e:
        logger.error(f"Error retrieving campaign record: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()    