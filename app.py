import datetime
from flask import Flask, render_template, request, json, make_response
import feedparser
import urllib3

app = Flask(__name__)

RSS_FEEDS = {
    'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn': 'http://rss.cnn.com/rss/edition.rss',
    'fox': 'http://feeds.foxnews.com/foxnews/latest',
    'iol': 'http://www.iol.co.za/cmlink/1.640'
}

DEFAULTS = {
    'publication': 'bbc',
    'city': 'London, Uk',
    'currency_from': 'GBP',
    'currency_to': 'USD'
}

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=68d5984d17bb1a50263b727b543bcd56"

CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=3daa4f22342e4cff9513629491d8ee39"


@app.route("/")
def home():
    """displays the home page with news and weather information"""
    # get news feed
    publication = get_value_with_fallback("publication")
    articles = get_news(publication)

    # get weather details
    city = get_value_with_fallback("city")
    weather = get_weather(city)

    # get currency details
    currency_from = get_value_with_fallback("currency_from")
    currency_to = get_value_with_fallback("currency_to")

    rate, currencies = get_rate(currency_from, currency_to)

    response = make_response(render_template("home.html",
                                             articles=articles,
                                             weather=weather,
                                             currency_from=currency_from,
                                             currency_to=currency_to,
                                             rate=rate,
                                             currencies=sorted(currencies)))

    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)

    return response


def get_news(query):
    """get news articles"""
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']


def get_weather(query):
    """gets weather details"""
    # remove any spaces in our query details
    query = query.strip()
    url = WEATHER_URL.format(query)

    # use the urllib3 HTTP Client library to fetch weather data from our api
    http = urllib3.PoolManager()
    api_request = http.request('GET', url)
    data = api_request.data
    parsed = json.loads(data)
    weather = None

    if parsed.get("weather"):
        weather = {
            "description": parsed["weather"][0]["description"],
            "temperature": parsed["main"]["temp"],
            "city": parsed["name"],
            'country': parsed['sys']['country']
        }

    return weather


def get_rate(frm, to):
    """returns the current exchange rates"""
    # use the urllib3 HTTP Client library to fetch weather data from our api
    http = urllib3.PoolManager()
    api_request = http.request('GET', CURRENCY_URL)
    all_currency = api_request.data
    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())

    return (to_rate / frm_rate, parsed.keys())


def get_value_with_fallback(key):
    """returns the overall value to display to a user"""
    if request.args.get(key):
        return request.args.get(key)

    if request.cookies.get(key):
        return request.cookies.get(key)

    return DEFAULTS[key]


if __name__ == "__main__":
    app.run(port=5000, debug=True)
