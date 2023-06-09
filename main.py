#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess, json, apikey	
from Adafruit_IO import Client, Feed

#Setup for Adafuit_IO
ADAFRUIT_IO_KEY = apikey.ADAFRUIT_IO_KEY
ADAFRUIT_IO_USERNAME = apikey.ADAFRUIT_IO_USERNAME
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

def run_speedtest():
   #Run Speedtest.net CLI and output as JSON data
   stdoutdata = subprocess.getoutput("speedtest -f json")
   try:
      results = json.loads(stdoutdata)
      return(results)
   except ValueError:
      results = "Error"
      pass
   return(results)

def decode_upload():
   download = results["download"]["bandwidth"] 
   upload = results["upload"]["bandwidth"]
   pings = results["ping"]["high"]
   jit = results["ping"]["jitter"]
   lat = results["ping"]["latency"]
   isp = results["isp"]
   #Format Data into English units
   down = str(round(download / 125000, 2))
   up = str(round(upload / 125000, 2))
   #Send Data to Adafruit IO
   upload = aio.feeds("speedtesting.up")
   download = aio.feeds("speedtesting.down")
   ping = aio.feeds("speedtesting.ping")
   latency = aio.feeds("speedtesting.lat")
   jitter = aio.feeds("speedtesting.jit")
   aio.send(upload.key, up)
   aio.send(download.key, down)
   aio.send(ping.key, pings)
   aio.send(jitter.key, jit)
   aio.send(latency.key, lat)

if __name__ == '__main__':
   results=run_speedtest()
   if (results != 'Error'):
      #print("Running")
      decode_upload()
   else :
      pass
      #print("Error")
