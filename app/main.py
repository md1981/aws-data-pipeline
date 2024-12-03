import os
import boto3
import psycopg2
from psycopg2 import sql
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_data(data):
    # Placeholder for more complex data processing
    return data.upper()

def main():
    try:
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
        try:
            response = s3.list_objects_v2(Bucket=bucket_name)
        except boto3.exceptions.BotoClientError as e:
            logger.error(f"Error listing objects in S3 bucket: {e}")
            raise

        for obj in response.get('Contents', []):
            try:
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

                logger.info(f"Processed and stored data from {obj['Key']}")
            except Exception as e:
                logger.error(f"Error processing {obj['Key']}: {e}")
                conn.rollback()

    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    main()

