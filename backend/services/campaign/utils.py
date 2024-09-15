import psycopg2
import uuid

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
        db_endpoint = "flaskpostgresdb.cv6ue4wqkpyw.us-east-1.rds.amazonaws.com"
        db_name = "flaskpostgresdb"
        db_user = "dbadmin"
        db_password = "Acc123$$"
        db_port = 5432

        conn = psycopg2.connect(
            host=db_endpoint,
            database=db_name,
            user=db_user,
            password=db_password,
            port=db_port
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
        db_endpoint = "flaskpostgresdb.cv6ue4wqkpyw.us-east-1.rds.amazonaws.com"
        db_name = "flaskpostgresdb"
        db_user = "dbadmin"
        db_password = "Acc1234$$"
        db_port = 5432

        conn = psycopg2.connect(
            host=db_endpoint,
            database=db_name,
            user=db_user,
            password=db_password,
            port=db_port
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

# Example record to be inserted
record = {
    "client_id": "123",
    "prod_id": "456",
    "campaign_type": "email",
    "length": 30,
    "target_demographic": "18-25"
}


# Insert the record into the PostgreSQL RDS instance with an auto-generated campaign_id
insert_record_into_rds(record)