from json import dumps
from kafka import KafkaProducer
from datetime import datetime
from requests import get
from time import sleep


def getStockData():
    now = datetime.today().date()
    start = datetime(2022, 8, 4).date()
    token = input("stockdata.org API-key: ")
    response = get(f'https://api.stockdata.org/v1/data/eod?symbols=AAPL&api_token={token}&date_from={start}&date_to={now}')
    response = response.json()
    data = response.get('data')
    return data

producer = KafkaProducer(
    bootstrap_servers=['localhost:9093'],
    value_serializer=lambda x: dumps(x).encode('utf-8'),
    api_version=(3,2,1)
)

data = getStockData()
for entry in data:
    day = {
        "apple_price": entry.get('close'),
        "date": str(
            datetime.strptime(
                entry.get('date'), '%Y-%m-%dT%H:%M:%S.%fZ'
            ).date()),
        "volume": entry.get('volume'),
        "high": entry.get("high"),
        "low": entry.get("low"),
        "open": entry.get("open")
    }
    print(dumps(day))
    producer.send('stockdata', value=day)
    sleep(1)


