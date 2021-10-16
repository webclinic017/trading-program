import bybit
import config

class Connect: 
    def make_connection(self):

        api_key = "SAanPVFbRIsXJ2Y9vb"
        api_secret = "Q0a59ZtKZsGOmUQHIOb7K0s96mFhTDhrkV3r"
        client = bybit.bybit(test=False, api_key=api_key, api_secret=api_secret)
        return client

