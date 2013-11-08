from urllib.error import URLError
from urllib.request import urlopen, Request

URL = 'http://finance.yahoo.com/d/quotes.csv?e=.csv&f=sl1d1t1&s={currency}=X'


def main(currency):
    request = Request(URL.format(currency=currency))
    value = 0.0000
    try:
        response = urlopen(request)
        result = response.read()
        value = str(result).split(",")[1]
    except URLError:
        pass
    return value


if __name__ == "__main__":
    main("EURUSD")