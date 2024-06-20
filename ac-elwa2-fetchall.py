import requests
from influxdb import InfluxDBClient

# Configure InfluxDB connection variables
host = "127.0.0.1"
port = 8086
username = "elwa"
password = "smart"
database = "ac_elwa2"

# URL of the web request
url = 'http://192.168.2.225/data.jsn'

# Perform the web request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON data
    data = response.json()

    # Extract and format the fields as necessary
    data['temp1'] = data['temp1'] / 10.0  # Convert temp1 from 552 to 55.2
    data['temp2'] = data['temp2'] / 10.0  # Convert temp1 from 552 to 55.2

    # Filter out key-value pairs where the value is null
    filtered_data = {k: v for k, v in data.items() if v is not None and k != "wifi_list"}

    # Flatten wifi_list
    wifi_list = data.get("wifi_list", [])
    for i, wifi in enumerate(wifi_list):
        for key, value in wifi.items():
            filtered_data[f"wifi_{i+1}_{key}"] = value

    # Prepare the data point
    json_body = [
        {
            "measurement": "elwa_data",
            "tags": {
                "device": filtered_data['device']
            },
            "fields": filtered_data
        }
    ]


    # Initialize the InfluxDB client
    client = InfluxDBClient(host=host, port=port, username=username, password=password, database=database)

    # Write the data point to InfluxDB
    client.write_points(json_body, time_precision='m')

    print("Data inserted successfully.")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
