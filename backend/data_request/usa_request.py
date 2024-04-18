from tenacity import retry, stop_after_attempt, wait_random
import yfinance as yf
import pandas as pd

tickers_list_USA = ['AAPL', 'NVDA', 'TSLA', 'META', 'GOOG', 'NFLX', 'V', 'IBM', 'MU', 'BA', 'AXP']


@retry(stop=stop_after_attempt(7), wait=wait_random(min=5, max=10))
def __get_from_yf(ticker, dt_start, dt_end):
    return yf.download(ticker, dt_start, dt_end)[['Open', 'Close', 'High', 'Low', 'Volume']]


def get_usa_data(dt_start, dt_end):
    data_USA = []
    for ticker in tickers_list_USA:
        data_USA.append(__get_from_yf(ticker, dt_start, dt_end))

    res_USA = pd.concat(data_USA, axis=1).resample('D').ffill()
    return res_USA
