from weather import Weather, Unit
from config import YAHOO_WOEID

def get_forecast():
    weather = Weather(unit=Unit.CELSIUS)
    lookup = weather.lookup(YAHOO_WOEID)
    return 'Today\'s forecast is {} with a high of {} degrees and a low of {} degrees. '.format(lookup.forecast[0].text, lookup.forecast[0].high, lookup.forecast[0].low)
