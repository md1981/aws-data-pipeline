import os
import boto3
import psycopg2
from psycopg2 import sql

def process_data(data):
    # Dummy processing function
    return data.upper()

def main():
    # Set up S3 client
    s3 = boto3.client('s3')
    bucket_name = os.environ['S3_BUCKET']

    # Set up database connection
    conn = psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD']
    )
    cur = conn.cursor()

    # Create table if not exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS processed_data (
            id SERIAL PRIMARY KEY,
            original_data TEXT,
            processed_data TEXT
        )
    """)
    conn.commit()

    # List objects in the S3 bucket
    response = s3.list_objects_v2(Bucket=bucket_name)

    for obj in response.get('Contents', []):
        # Get object content
        file_content = s3.get_object(Bucket=bucket_name, Key=obj['Key'])['Body'].read().decode('utf-8')

        # Process data
        processed_data = process_data(file_content)

        # Insert into database
        cur.execute(
            sql.SQL("INSERT INTO processed_data (original_data, processed_data) VALUES (%s, %s)"),
            (file_content, processed_data)
        )
        conn.commit()

        print(f"Processed and stored data from {obj['Key']}")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()