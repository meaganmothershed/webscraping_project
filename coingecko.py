import requests 
from twilio.rest import Client

account_sid = 'AC1522797373184cc20398a377a21dc40d'
auth_token = '3a1302b0cc6bc4affe053e96278d7407'
twilio_phone_no = '+18559355350'
phone_no = '8324991744'

def top5_cryptos():
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {'vs_currency': 'usd',
              'order': 'market_cap_desc',
              'per_page': 5, 'page': 1,
              'sparkline': False,
              'price_change_percentage': '24h'}
    
    request = requests.get(url, params=params)

    if request.status_code == 200:
        return request.json()
    else:
        print('Unable to get data.')
        return None
    
def twilio_message(text):
    try:
        client = Client(account_sid, auth_token)
        text = client.messages.create(body = text, from_ = twilio_phone_no, to = phone_no)

        print(f'Twilio message sent. SID: {text.sid}')
    except Exception as exception:
        print(f'Error sending message: {exception}')

def crypto_scraping(coingecko):
    for rec in coingecko:
        name = rec['name']
        symbol = rec['symbol'].upper()
        curr_price = rec['current_price']
        change_price = rec['price_change_percentage_24h']

        corr_price = (1 + change_price / 100) * curr_price

        print(f'Name: {name}')
        print(f'Symbol: {symbol}')
        print(f'Current Price: ${curr_price:.2f}')
        print(f'Price Change % in 24hrs: {change_price:.2f}%')
        print(f'Corresponding Price: ${corr_price:.2f}')
        input()

        if name == 'Ethereum' and curr_price > 2000:
            text_message = f'Price of Ethereum is more than $2,000! The current price is ${curr_price:.2f}.'
            twilio_message(text_message)

def main():
    coingecko = top5_cryptos()
    if coingecko:
        crypto_scraping(coingecko)

if __name__ == "__main__":
    main()