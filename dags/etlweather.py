from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task
import json
from datetime import datetime, timedelta

# Constants for latitude, longitude, and connection IDs
LATITUDE = '51.5074'
LONGITUDE = '-0.1278'
POSTGRES_CONN_ID = 'postgres_default'
API_CONN_ID = 'open_meteo_api'

# Default arguments for the DAG (owner and dynamic start_date)
default_args = {
    'owner': 'airflow',
    'start_date': datetime.now() - timedelta(days=1),  # Start 1 day ago
}

# Define the DAG
with DAG(dag_id='etl_weather_data',
         default_args=default_args,
         schedule='@daily',  # Run daily
         catchup=False) as dag:

    # Task: Extract weather data from the API
    @task
    def extract_weather_data():
        """Extract weather data from Open Meteo API."""
        http_hook = HttpHook(http_conn_id=API_CONN_ID, method='GET')  # Initialize HttpHook
        endpoint = f"/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true"
        response = http_hook.run(endpoint)  # Make API request
        if response.status_code == 200:
            return response.json()  # Return response JSON if successful
        else:
            raise Exception(f"Failed to fetch data: {response.status_code}")  # Raise exception if failed

    # Task: Transform the raw weather data
    @task
    def transform_weather_data(weather_data: dict) -> dict:
        """Transform weather data."""
        current_weather = weather_data['current_weather']  # Focus on current weather section
        transformed_data = {
            'latitude': float(LATITUDE),
            'longitude': float(LONGITUDE),
            'temperature': current_weather['temperature'],
            'windspeed': current_weather['windspeed'],
            'winddirection': current_weather['winddirection'],
            'weathercode': current_weather['weathercode']
        }
        return transformed_data  # Return flattened and simplified data

    # Task: Load the transformed data into Postgres
    @task
    def load_weather_data(weather_data: dict):
        """Load weather data into Postgres."""
        postgres_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)  # Initialize PostgresHook
        conn = postgres_hook.get_conn()  # Get raw connection
        cursor = conn.cursor()

        # Create the table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_data (
                id SERIAL PRIMARY KEY,
                latitude FLOAT NOT NULL,
                longitude FLOAT NOT NULL,
                temperature FLOAT NOT NULL,
                windspeed FLOAT NOT NULL,
                winddirection INT NOT NULL,
                weathercode INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Insert the new weather data
        cursor.execute("""
            INSERT INTO weather_data (latitude, longitude, temperature, windspeed, winddirection, weathercode)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (
            weather_data['latitude'],
            weather_data['longitude'],
            weather_data['temperature'],
            weather_data['windspeed'],
            weather_data['winddirection'],
            weather_data['weathercode']
        ))

        conn.commit()  # Commit changes
        cursor.close()  # Close cursor
        conn.close()    # Close connection

    # Define the task execution order
    raw_weather_data = extract_weather_data()  # Extract data first
    processed_weather_data = transform_weather_data(raw_weather_data)  # Then transform it
    load_weather_data(processed_weather_data)  # Finally load it into database
