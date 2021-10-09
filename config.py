from binance.client import Client
import config

class Connect: 
    def make_connection(self):

        api_key = "A1ZTZABu2Q60oKCXV5Of9AbLr2Uitl5gaZV6prAR7XD9RFYtDYEnaDWvU4yKPpDh"
        api_secret = "7wCUCMnJwI0gH9iNnzkgaY1yKilMubIeWUGILBXGJWzQLxDQ9bJ1cpSKv0Oyvttx"

        return Client(api_key, api_secret)