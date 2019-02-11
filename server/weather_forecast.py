import requests

from config import ACCUWEATHER_LOCATION_KEY
from secrets import ACCUWEATHER_API_KEY

def get_forecast():
    resp = send_req()
    minimum = int(round(resp['DailyForecasts'][0]['Temperature']['Minimum']['Value']))
    maximum = int(round(resp['DailyForecasts'][0]['Temperature']['Maximum']['Value']))
    phrase = resp['DailyForecasts'][0]['Day']['IconPhrase']
    return 'Today\'s forecast is {} with a high of {} degrees and a low of {} degrees. '.format(phrase, maximum, minimum)

def send_req():
    payload = {
        'apikey': ACCUWEATHER_API_KEY,
        'language': 'en-us',
        'details': 'false',
        'metric': 'true',
    }
    url = 'https://dataservice.accuweather.com/forecasts/v1/daily/1day/{}'.format(ACCUWEATHER_LOCATION_KEY)
    resp = requests.get(url, params=payload)
    return resp.json()
