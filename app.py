# main program
from flask import Flask
import os
import json
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta

app = Flask(__name__)

@app.route('/user/<userphrase>')
def getAirQuality(userphrase):
	inputtext = userphrase
	stationId = station(inputtext)
	url = "http://realtime-api.opendatanepal.com/airquality/api/latest?id="+str(stationId)+"&params=pm25,pm10,pm1,tsp&coordinate=false"
	response = requests.get(url)
	apidata = response.json()
	stationName = str(apidata["result"][0]["stationName"])
	tsp = "TSP : "+ str(apidata["result"][0]["params"]["tsp"][0]["value"]) + "\n"
	pm1 = "Pm1 : " + str(apidata["result"][0]["params"]["pm1"][0]["value"])+ "\n"
	pm2 = apidata["result"][0]["params"]["pm1"][0]["value"]
	pm25 = "Pm25 : " + str(apidata["result"][0]["params"]["pm25"][0]["value"])+ "\n"
	pm10 = "Pm10 : " + str(apidata["result"][0]["params"]["pm10"][0]["value"])+ "\n"
	dataTaken = apidata["result"][0]["params"]["pm10"][0]["datetime"].split('T')
	d1 = timeCalculate(dataTaken)
	current = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	currentTime = datetime.strptime(current,'%Y-%m-%d %H:%M:%S')
	diff = relativedelta(currentTime, d1)
	dataMessages = dataMessage(diff)
	apiDataExtracted ="The latest Air Quality data of " + stationName +" is: \n" + tsp + pm1 + pm25 + pm10 + "\n" + conclusion(pm2) + "\n"+ dataMessages+ "(" + str(d1) + ")" 
	return apiDataExtracted

def timeCalculate(dataTaken):
	dataTime = dataTaken[0] + " " + dataTaken[1].split('.')[0]
	datetime_object = datetime.strptime(dataTime,'%Y-%m-%d %H:%M:%S')
	d1 = datetime_object + timedelta(hours=5,minutes=45)
	return d1

def conclusion(pm2):
	if pm2 > 0 and pm2 < 51:
		conclusionMessage = "good."
	elif pm2 > 50 and pm2 < 101:
		conclusionMessage = "moderate."
	elif pm2 > 100 and pm2 < 151:
		conclusionMessage = "unhealthy for sensitive groups."
	elif pm2 > 150 and pm2 < 201:
		conclusionMessage = "unhealthy"
	elif pm2 > 200:
		conclusionMessage = "hazardous"
	return "The air quality is "+ conclusionMessage

def dataMessage(diff):
	message = "The data was taken "
	if diff.years > 0: 
		message += str(diff.years) + " years "
	if diff.months > 0: 
		message += str(diff.months) + " months "
	if diff.days > 0: 
		message += str(diff.days) + " days "
	if diff.hours > 0: 
		message += str(diff.hours) + " hours "
	if diff.minutes > 0: 
		message += str(diff.minutes) + " minutes "
	return message + 'ago '


def station(original):
	original = original.lower()
	if original == "bhaisipati":
		stationId = 37

	elif original == "bhaktpur":
		stationId = 29

	elif original == "dhmpkr":
		stationId = 28

	elif original == "dang":
		stationId = 9

	elif original == "dhulikhel":
		stationId = 40	

	elif original == "usemb":
		stationId = 33

	elif original == "gbspkr":
		stationId = 35

	elif original == "lumbini":
		stationId = 42

	elif original == "nepalgunj":
		stationId = 16

	elif original == "phodurktm":
		stationId = 11

	elif original == "pupkr":
		stationId = 43

	elif original == "pulchowk":
		stationId = 32

	elif original == "ratnapark":
		stationId = 36

	elif original == "sauraha":
		stationId = 34

	elif original == "simara":
		stationId = 7

	elif original == "surkhet":
		stationId = 26

	elif original == "dhankuta":
		stationId = 25

	elif original == "jhumka":
		stationId = 39

	elif original == "shankapark":
		stationId = 41

	return stationId

@app.route('/data/<userphrase>')
def getAirQuality(userphrase):
	stationId = userphrase
	url = "http://realtime-api.opendatanepal.com/airquality/api/latest?id="+str(stationId)+"&params=pm25,pm10,pm1,tsp&coordinate=false"
	response = requests.get(url)
	apidata = response.json()
	stationName = str(apidata["result"][0]["stationName"])
	tsp = "TSP : "+ str(apidata["result"][0]["params"]["tsp"][0]["value"]) + "\n"
	pm1 = "Pm1 : " + str(apidata["result"][0]["params"]["pm1"][0]["value"])+ "\n"
	pm2 = apidata["result"][0]["params"]["pm1"][0]["value"]
	pm25 = "Pm25 : " + str(apidata["result"][0]["params"]["pm25"][0]["value"])+ "\n"
	pm10 = "Pm10 : " + str(apidata["result"][0]["params"]["pm10"][0]["value"])+ "\n"
	dataTaken = apidata["result"][0]["params"]["pm10"][0]["datetime"].split('T')
	d1 = timeCalculate(dataTaken)
	current = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	currentTime = datetime.strptime(current,'%Y-%m-%d %H:%M:%S')
	diff = relativedelta(currentTime, d1)
	dataMessages = dataMessage(diff)
	apiDataExtracted ="The latest Air Quality data of " + stationName +" is: \n" + tsp + pm1 + pm25 + pm10 + "\n" + conclusion(pm2) + "\n"+ dataMessages+ "(" + str(d1) + ")" 
	return apiDataExtracted

@app.route('/')
def index():
	return "<h1> Welcome to our Server <h1>"

if __name__ == '__main__':
	app.run(threaded=True, port=5000)
