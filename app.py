# main program
from flask import Flask
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
	d1 = datetime_object + timedelta(hours=5,minutes=15)
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
	if original == "Bhaisipati":
		stationId = 37

	elif original == "Bhaktpur":
		stationId = 29

	elif original == "DHMPkr":
		stationId = 28

	elif original == "Dang":
		stationId = 9

	elif original == "Dhulikhel":
		stationId = 40	

	elif original == "USEmb":
		stationId = 33

	elif original == "GBSPkr":
		stationId = 35

	elif original == "Lumbini":
		stationId = 42

	elif original == "Nepalgunj":
		stationId = 16

	elif original == "PhoDurKtm":
		stationId = 11

	elif original == "PUPkr":
		stationId = 43

	elif original == "Pulchowk":
		stationId = 32

	elif original == "Ratnapark":
		stationId = 36

	elif original == "Sauraha":
		stationId = 34

	elif original == "Simara":
		stationId = 7

	elif original == "Surkhet":
		stationId = 26

	elif original == "Dhankuta":
		stationId = 25

	elif original == "Jhumka":
		stationId = 39

	elif original == "Shankapark":
		stationId = 41

	return stationId




if __name__ == '__main__':
	app.run()