import requests     # Module to fetch data from switches
import datetime     # Module to keep track of time
import time         # Module to make program wait for given amount of time
import json         # Module to convert variables of type string to dict
import csv          # Module to create and write .csv files

#from Plotting import *

startTime = datetime.datetime.today()
startTimeFileName = startTime.strftime("%Y-%m-%d")
currentTime = startTime

# Set parameters
duration = 40 * 60         # Set run time [s] (duration -> how the switch should stay turned on)
fileName = "../Data/Data" + "_" + startTimeFileName + ".csv"    # Set name of created .csv file
fieldNames = ['power', 'Ws', 'relay', 'temperature', 'time']

# Convert duration to time format
deltaTime = datetime.timedelta(seconds=duration)

# Calculate end time based on given duration
endTime = startTime + deltaTime

# Define the required urls to fetch data and current settings
url = ["http://192.168.0.22/api/v1/monitor", "http://192.168.0.22/report", "http://192.168.0.22/relay?state=1", "http://192.168.0.22/relay?state=0"]

settings = json.loads(requests.request("GET", url[0]).text)
switchEnabled = settings["enabled"]

data = json.loads(requests.request("GET", url[1]).text)
data["time"] = startTime

# Switch on for set duration
if settings["enabled"] is False:
    switchON = requests.request("GET", url[2]).text
    print(switchON)
    print('MyStrom switch has been turned on!')
else:
    keepON = requests.request("GET", url[2]).text
    raise Exception('The switch is already turned on!')

# Create and open .csv file
with open(fileName, 'w', newline='') as csvFile:

    writer = csv.DictWriter(csvFile, fieldnames=fieldNames)
    writer.writeheader()

count = 0

while currentTime < endTime:

    with open(fileName, 'a') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=fieldNames)
        print(data)
        # Write data to csv file
        writer.writerow(data)
        # Update state of switch (enabled or not)
        settings = json.loads(requests.request("GET", url[0]).text)
        switchEnabled = settings["enabled"]
        # Wait for 5 seconds (= sampling interval)
        time.sleep(0.5)
        # Fetch current data
        data = json.loads(requests.request("GET", url[1]).text)
        # Update current time
        currentTime = datetime.datetime.today()
        data["time"] = currentTime

    count += 1

switchOFF = requests.request("GET", url[3]).text

print('MyStrom switch has been turned off!')

exit()
