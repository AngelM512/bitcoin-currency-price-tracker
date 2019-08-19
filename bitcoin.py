import requests
import time
from datetime import datetime

BITCOIN_TRESHOLD = 10000
BITCOIN_API = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
IFTTT_WBHOOK = 'https://maker.ifttt.com/trigger/{}/with/key/dJJk_WaFlDWgoOnpFnr2pamXJN7z2RxZCzsZdkyc7Kq'

def get_latest_bitcoin_price():
    response = requests.get(BITCOIN_API).json()
    return float(response[0]['price_usd'])

def show_bitcoin_inf(event, value):
    data = {'value1':value}
    url = IFTTT_WBHOOK.format(event)
    requests.post(url, json=data)


def format_bitcoin_records(bitcoin_records):
    blocks = []
    # Formats the date into a string: '24.02.2018 15:09'
    for record in bitcoin_records:
        date = record['date'].strftime('%d.%m.%Y %H:%M')
        price = record['price']
        block = 'Date: {}, Price:<b>{}</b>'.format(date, price)
        blocks.append(block)

    return '<br>'.join(blocks)


def main():
    bitcoin_records = []
    while True:
        price = get_latest_bitcoin_price()
        date = datetime.now()
        bitcoin_records.append({'date':date, 'price':price})
        # notify user
        print("bitcoin_records= ",bitcoin_records)
        print()
        if BITCOIN_TRESHOLD <= 10000:
            show_bitcoin_inf('emergency_bitcoin_price', price)
        if len(bitcoin_records) == 3:
            show_bitcoin_inf('bitcoin_price_update',
                            format_bitcoin_records(bitcoin_records))
            #reset records
            bitcoin_records = []

        time.sleep(10)



if __name__ == '__main__':
    main()
