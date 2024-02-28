from okx.api import API
from okx.app.utils import eprint

if __name__ == '__main__':
    proxy_host = 'http://43.156.53.213/'  # OKX_resender地址
    api = API(proxy_host=proxy_host)
    ticker_result = api.market.get_ticker(instId='BTC-USDT')
    eprint(ticker_result, length=20)
