from requests import get
from kafka import KafkaProducer
from json import dumps
from time import sleep

producer = KafkaProducer(
    bootstrap_servers=['localhost:9093'],
    value_serializer=lambda x: dumps(x).encode('utf-8'),
    api_version=(3,2,1)
)

api_key = input("RapidAPI-key: ")

url = "https://forecast9.p.rapidapi.com/rapidapi/forecast/New%20York/summary/"

headers = {
	"X-RapidAPI-Key": api_key,
	"X-RapidAPI-Host": "forecast9.p.rapidapi.com"
}

response = get(url, headers=headers)
response = response.json()['forecast']['items']
for item in response:
    tavg = (item.get('wind').get('min', 0) + item.get('wind').get('max', 0))/2
    data = {
        "DATE": item.get('date'),
        "SNOW": item.get('freshSnow', 0),
        "SNWD": item.get('snowHeight', 0),
        "PRCP": item.get('prec').get('sum', 0),
        "TMIN": item.get('temperature').get('min'),
        "TMAX": item.get('temperature').get('max'),
        "TAVG": tavg,
        "AWND": (item.get('wind').get('min', 0) + item.get('wind').get('max', 0))/10,
        "STATION": 'New York',
    }
    data = {k: 0.0 if not v else v for k, v in data.items() }
    print(dumps(data))
    producer.send('weatherdata', value=data)
    sleep(1)
