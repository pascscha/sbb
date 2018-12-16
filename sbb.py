import sys
from datetime import datetime

import pytz
import requests

from coloring import *

if __name__ == "__main__":
    show_tag("tag.txt")
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

    elif len(sys.argv) == 1:
        fromStation = input("From: ")
        toStation = input("To: ")
        time = input("Time: ")
        if time != "":
            departure_time = time
        else:
            departure_time = datetime.now().strftime(time_format)

    else:
        print("Invalid number of arguments")
        exit(0)

    print("Verbindungen werden geladen...",end="", flush=True)
    parameters = {"from": fromStation, "to": toStation, "time": departure_time, "limit": 10}
    response = requests.get("http://transport.opendata.ch/v1/connections", params=parameters)
    data = response.json()
    print("\r",end="")

    connections = data['connections']

    printdata = []
    for i in range(0, min(10, len(connections))):
        connection = connections[i]
        fromStation = connection['from']['station']['name']
        fromPlatform = connection['from']['platform']
        departure = datetime.fromtimestamp(connection['from']['departureTimestamp'], tz=timezone).strftime(time_format)
        toStation = connection['to']['station']['name']
        toPlatform = connection['to']['platform']
        arrival = datetime.fromtimestamp(connection['to']['arrivalTimestamp'], tz=timezone).strftime(time_format)

        printdata.append([fromStation, departure, fromPlatform, toStation, arrival, toPlatform])

    lengths = [3, 7, 5, 4, 7, 5]
    for i in range(len(printdata)):
        for j in range(len(printdata[i])):
            if printdata[i][j] == None:
                printdata[i][j] = ""
            elif len(lengths) < j + 1:
                lengths.append(len(printdata[i][j]))
            elif lengths[j] < len(printdata[i][j]):
                lengths[j] = len(printdata[i][j])

    form = ""
    for i in range(len(lengths)):
        form = form + "{:^" + str(2 + lengths[i]) + "}"
        if i == len(lengths) / 2 - 1:
            form = form + "|"

    print(colorize("{BG_BLACK}" + form.format("Von", "Abfahrt", "Gleis", "Nach", "Ankunft", "Gleis") + "{BG_DEFAULT}"))

    for d in printdata:
        print(colorize("{BG_BLUE}" + form.format(d[0], d[1], d[2], d[3], d[4], d[5]) + "{BG_DEFAULT}"))

    print()
