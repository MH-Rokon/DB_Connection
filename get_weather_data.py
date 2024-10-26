import json
import psycopg2
from psycopg2 import sql

# Database connection details
host = "dpg-csdvkr3v2p9s73b2bkog-a"
port = "5432"
dbname = "preventers"
user = "preventers_user"
password = "xR7u0DpZsQRdyArWZGmrCQ7zMrH53lQp"

try:
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

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

    # Check if data was found
    if data:
        # Output data in JSON format
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
    print(json.dumps({"error": "Connection or query failed: " + str(e)}))

finally:
    # Close the cursor and connection
    if cursor:
        cursor.close()
    if conn:
        conn.close()
