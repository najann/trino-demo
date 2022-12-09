from time import sleep
from json import dumps
from kafka import KafkaProducer
from datetime import datetime, timedelta
from requests import get


def getWeatherData(now):
    date = (now + timedelta(days=-1)).date()
    date = date.strftime("%Y-%m-%d")
    start = datetime(2022, 8, 4).date()
    response = get(f'https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&dataTypes=PRCP,SNWD,SNOW,TSUN,TAVG,TMAX,TMIN,AWND&stations=USW00094789&startDate={start}&endDate={date}&format=json&units=metric')
    response = response.json()
    return response


producer = KafkaProducer(
    bootstrap_servers=['localhost:9093'],
    value_serializer=lambda x: dumps(x).encode('utf-8'),
    api_version=(3,2,1)
)

while True:
    now = datetime.today()
    data = getWeatherData(now)
    for entry in data:
        day = {k: float(v) if v.replace('.', '', 1).isdigit() else v for k, v in entry.items() }
        print(dumps(day))
        producer.send('weatherdata', value=day)
    sleep(864001)


