### MyPv AC ELWA 2

Diese Skript liest Daten aus den MyPv AC-ELWA 2 aus und schreibt diese in eine InfluxDB.

Das auslesen wird über ein WebRequest gemacht die Daten stehen am AC-ELWA 2 als JSON File zu verfügung. Geprüft werden kann das mit curl/wget oder einem Browser:

```bash
# curl http://192.168.2.225/data.jsn
{
"device":"AC ELWA 2",
"fwversion":"e0000901",
"psversion":"ep107",
"coversion":"ec103",
"fsetup":0,
"p1_s":240,
"p1_v":"0000901",
"p2_s":255,
"p2_v":"null",
"p_co_s":255,
"p_co_v":"null",
"p_ps_s":240,
"p_ps_v":"ep107",
"power_system":null,
"screen_mode_flag":1,
"power_elwa2":136,
"power_solar":136,
"power_grid":0,
"power1_solar":136,
"power1_grid":0,
"power2_solar":0,
"power2_grid":0,
"power3_solar":0,
"power3_grid":0,
"rel1_out":0,
"rel_selv":0,
"temp1":529,
"temp2":0,
```

Das Skript parsed alle Daten und trägt diese in eine InfluxDB ein. Die JSON File ist nested und wird durch das Skript noch zu einer Flachen JSON umgebaut, da dies sonst nicht von InfluxDB unterstützt wird. Weiterhin wird die Temperatur direkt auf die benötigte Notation umgerechnet:

```python3
    # Extract and format the fields as necessary
    data['temp1'] = data['temp1'] / 10.0  # Convert temp1 from 552 to 55.2
    data['temp2'] = data['temp2'] / 10.0  # Convert temp1 from 552 to 55.2

    # Flatten wifi_list
    wifi_list = data.get("wifi_list", [])
    for i, wifi in enumerate(wifi_list):
        for key, value in wifi.items():
            filtered_data[f"wifi_{i+1}_{key}"] = value
```

Die Daten sehen dann wie folgt in der InfluxDB aus:

```
time       blockactive boostactive cloudstate co_upd_state coversion coversionlatest ctrl_errors ctrlstate             cur_dns     cur_eth_mode cur_gw      cur_ip        cur_sn        date     debug_ip device    device_1  ecarstate fan_speed freq  fsetup fwversion fwversionlatest legboostnext loctime  meter1_ip meter2_ip meter3_ip meter4_ip meter5_ip meter6_ip meter_ssid mss10 mss11 mss2 mss3 mss4 mss5 mss6 mss7 mss8 mss9 p1_s p1_v    p2_s p2_v p_co_s p_co_v p_ps_s p_ps_v power1_grid power1_solar power2_grid power2_solar power3_grid power3_solar power_elwa2 power_grid power_solar ps_state ps_upd_state psversion psversionlatest rel1_out rel_selv screen_mode_flag temp1 temp2 temp_ps unixtime   upd_state uptime volt_aux volt_mains warnings wifi_10_signal wifi_10_ssid wifi_11_signal wifi_11_ssid wifi_12_signal wifi_12_ssid wifi_13_signal wifi_13_ssid wifi_14_signal wifi_14_ssid wifi_15_signal wifi_15_ssid wifi_16_signal wifi_16_ssid wifi_1_signal wifi_1_ssid wifi_2_signal wifi_2_ssid wifi_3_signal wifi_3_ssid wifi_4_signal wifi_4_ssid wifi_5_signal wifi_5_ssid wifi_6_signal wifi_6_ssid wifi_7_signal wifi_7_ssid wifi_8_signal wifi_8_ssid wifi_9_signal wifi_9_ssid wifi_signal
----       ----------- ----------- ---------- ------------ --------- --------------- ----------- ---------             -------     ------------ ------      ------        ------        ----     -------- ------    --------  --------- --------- ----  ------ --------- --------------- ------------ -------  --------- --------- --------- --------- --------- --------- ---------- ----- ----- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----    ---- ---- ------ ------ ------ ------ ----------- ------------ ----------- ------------ ----------- ------------ ----------- ---------- ----------- -------- ------------ --------- --------------- -------- -------- ---------------- ----- ----- ------- --------   --------- ------ -------- ---------- -------- -------------- ------------ -------------- ------------ -------------- ------------ -------------- ------------ -------------- ------------ -------------- ------------ -------------- ------------ ------------- ----------- ------------- ----------- ------------- ----------- ------------- ----------- ------------- ----------- ------------- ----------- ------------- ----------- ------------- ----------- ------------- ----------- -----------
1718714979 0           0           4          0            ec103     ec103           0           Conn. to Home Manager 192.168.2.1 0            192.168.2.1 192.168.2.225 255.255.255.0 18.06.24 0.0.0.0  AC ELWA 2 AC ELWA 2 null      0         49998 0      e0000901  e0000901        null         14:49:39 null      null      null      null      null      null      null       null  null  null null null null null null null null 240  0000901 255  null 255    null   240    ep107  0           4            0           0            0           0            4           0          4           0        0            ep107     ep107           0        0        1                53.4  0     411     1718714979 0         25     4        232        0        0                           0                           0                           0                           0                           0                           0                           0                         0                         0                         0                         0                         0                         0                         0                         0                         0
```

Dies kann nun in Grafana ausgelesen und visualiziert werden.

## Installation

```bash
pip install influxdb requests
```

## Anlegen der InfluxDB
```
influx -execute "create database ac_elwa2"
influx -execute "SHOW DATABASES"
influx -execute "CREATE USER elwa WITH PASSWORD 'smart' WITH ALL PRIVILEGES"
influx -execute "grant all privileges on ac_elwa2 to elwa"
```

## Crontab
Ich lese die Daten jede Minute mittels eines crontabs aus.

```bash
# crontab -e
*/1 * * * * /usr/bin/python3 /root/ac-elwa2/ac-elwa2-fetchall.py
```

## Vor dem Starten muss die IP-Adresse im Skript auf die vom eueren AC-ELWA 2 geändert werden.








