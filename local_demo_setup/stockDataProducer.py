from time import sleep
from json import dumps
from kafka import KafkaProducer
from datetime import datetime
from requests import get


def getStockData():
    token = input("stockdata.org API-key: ")
    response = get(f'https://api.stockdata.org/v1/data/quote?symbols=AAPL&api_token={token}')
    response = response.json()
    data = response.get('data')[0]
    try:
        data = {
            "apple_price": data.get('price'),
            "date": str(
                datetime.strptime(
                    data.get('previous_close_price_time'), '%Y-%m-%dT%H:%M:%S.%f' #'2022-08-25T01:01:01.000000'
                ).date()),
            "volume": data.get('volume'),
            "high": data.get("day_high"),
            "low": data.get("day_low"),
            "open": data.get("day_open")
        }
    except TypeError:
        data = {"apple": 0}
    return data


def getTimes():
    open = datetime.today().replace(hour=15, minute=30, second=0, microsecond=0)
    close = datetime.today().replace(hour=22, minute=00, second=0, microsecond=0)
    now = datetime.today()
    return open, close, now

producer = KafkaProducer(
    bootstrap_servers=['localhost:9093'],
    value_serializer=lambda x: dumps(x).encode('utf-8'),
    api_version=(3,2,1)
)

open, close, now = getTimes()
data = getStockData()

while True:
    open, close, now = getTimes()

    if now >= open and now <= close:
        data = getStockData()

    print(dumps(data))
    producer.send('stockdata', value=data)
    sleep(60)


