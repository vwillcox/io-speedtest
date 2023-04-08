#!/usr/bin/python3
import subprocess
import json
from Adafruit_IO import Client, Feed
import apikey

#Setup for Adafuit_IO

ADAFRUIT_IO_KEY = apikey.ADAFRUIT_IO_KEY
ADAFRUIT_IO_USERNAME = apikey.ADAFRUIT_IO_USERNAME

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

#Run Speedtest.net CLI and output as JSON data
stdoutdata = subprocess.getoutput("speedtest -f json")
#print(stdoutdata.split()[0])
results = json.loads(stdoutdata)
for key in results:
   download = results["download"]["bandwidth"] 
   upload = results["upload"]["bandwidth"]
   isp = results["isp"]

#Format Data into English units
down = str(round(download / 125000, 2))
up = str(round(upload / 125000, 2))

#print("Download: "+ down + "Mbps")
#print("Upload: " + up + "Mbps")
#print("Internet Provider: " + isp)

#Send Data to Adafruit IO

upload = aio.feeds("speedtesting.up")
download = aio.feeds("speedtesting.down")


aio.send(upload.key, up)
aio.send(download.key, down)
