import requests
from influxdb import InfluxDBClient
from datetime import datetime
import time

# Configure InfluxDB connection variables
host = "127.0.0.1"
port = 8086
user = "elwa"
password = "smart"
dbname = "ac_elwa2"

# URL of the web request
url = 'http://192.168.2.225/data.jsn'

# Perform the web request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON data
    data = response.json()

    # Extract the required fields
    power_elwa2 = data['power_elwa2']    # Benötigte Watt Gesamt
    power_solar = data['power_solar']    # Benötigte Watt Solar
    power_grid = data['power_grid']      # Benötigte Watt Grid / Netzbezug
    temp1 = data['temp1'] / 10.0         # Convert temp1 from 552 to 55.2 / Aktuelle gemessen Temperatur Sensor 1
    uptime = data['uptime']              # Anzahl Anschaltungen

    # Print the extracted values
    print(f"unixtime: {unixtime}")
    print(f"power_elwa2: {power_elwa2}")
    print(f"power_solar: {power_solar}")
    print(f"power_grid: {power_grid}")
    print(f"temp1: {temp1}")
    print(f"uptime: {uptime}")

    # Initialize the InfluxDB client
    client = InfluxDBClient(host=host, port=port, username=user, password=password, database=dbname)

    # Prepare the data point
    json_body = [
        {
            "measurement": "elwa_data",
            "tags": {
                "device": "AC ELWA 2"
            },
            "fields": {                
                "power_elwa2": power_elwa2,
                "power_solar": power_solar,
                "power_grid": power_grid,
                "temp1": temp1,
                "uptime": uptime
            }
        }
    ]

    # Write the data point to InfluxDB
    client.write_points(json_body, time_precision='m')


else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
