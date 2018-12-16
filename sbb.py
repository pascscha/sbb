import sys
from datetime import datetime

import pytz
import requests

timezone = pytz.timezone('Etc/GMT-1')
time_format = "%H:%M"

if len(sys.argv) == 3:
    fromStation = sys.argv[1]
    toStation = sys.argv[2]
    departure_time = datetime.now().strftime(time_format)

elif len(sys.argv) == 4:
    fromStation = sys.argv[1]
    toStation = sys.argv[2]
    departure_time = sys.argv[3]

else:
    print("Invalid number of arguments")
    exit(0)

parameters = {"from": fromStation, "to": toStation, "time": departure_time, "limit": 10}

response = requests.get("http://transport.opendata.ch/v1/connections", params=parameters)
data = response.json()

connections = data['connections']

format = "{:^15}{:^7}{:^7}"
print((format + "|" + format).format("Von", "Abfahrt", "Gleis", "Nach", "Ankunft", "Gleis"))
for i in range(0, min(10, len(connections))):
    connection = connections[i]
    fromStation = connection['from']['station']['name']
    fromPlatform = connection['from']['platform']
    departure = datetime.fromtimestamp(connection['from']['departureTimestamp'], tz=timezone).strftime(time_format)
    toStation = connection['to']['station']['name']
    toPlatform = connection['to']['platform']
    arrival = datetime.fromtimestamp(connection['to']['arrivalTimestamp'], tz=timezone).strftime(time_format)

    print((format + "|" + format).format(fromStation, departure, fromPlatform, toStation, arrival, toPlatform))
