import json
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Database connection details from environment variables
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
dbname = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

try:
    # Ensure environment variables are loaded
    if not all([host, port, dbname, user, password]):
        raise ValueError("Some environment variables for DB connection are missing.")

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

    # Use a context manager for the cursor
    with conn.cursor() as cursor:
        # Set the region_id to retrieve
        region_id = 2

        # SQL query to retrieve the latest weather data for the specified region_id
        query = sql.SQL(""" 
            SELECT temperature, wind_speed, humidity, current_instruction 
            FROM weather_data 
            WHERE region_id = %s 
            AND id = (SELECT MAX(id) FROM weather_data WHERE region_id = %s); 
        """)

        # Execute the query
        cursor.execute(query, (region_id, region_id))

        # Fetch the result
        data = cursor.fetchone()

        # Check if data was found and output in JSON format
        if data:
            ordered_data = {
                'temperature': data[0],
                'wind_speed': data[1],
                'humidity': data[2],
                'current_instruction': data[3],
            }
            print(json.dumps(ordered_data))
        else:
            print(json.dumps({"error": "No data found"}))

except Exception as e:
    # Handle connection and query errors
    print(json.dumps({"error": f"Connection or query failed: {str(e)}"}))

finally:
    # Close the connection
    if conn:
        conn.close()
