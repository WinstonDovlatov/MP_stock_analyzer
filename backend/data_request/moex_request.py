from tenacity import retry, stop_after_attempt, wait_random
import pandas as pd
import requests
from utils import str_to_dt
from datetime import timedelta

tickers_list_RU = ['SBER', 'ROSN', 'LKOH', 'GAZP', 'NVTK', 'GMKN', 'PLZL', 'YNDX', 'VTBR']


def get_moex_data(dt_start, dt_end):
    data_ru = []
    for ticker in tickers_list_RU:
        cur = __get_from_moex_ticker(ticker, dt_start, dt_end)[['open', 'close', 'high', 'low', 'volume']]
        data_ru.append(cur)
    return pd.concat(data_ru, axis=1)


@retry(stop=stop_after_attempt(10), wait=wait_random(min=10, max=20))
def __get_from_moex_batch(ticker, date_from, date_to):
    raw_data = requests.get(
        f'http://iss.moex.com/iss/engines/stock/markets/shares/securities/{ticker}/candles.json?from={date_from}&till={date_to}&interval=24').json()
    data = [{k: r[i] for i, k in enumerate(raw_data['candles']['columns'])} for r in raw_data['candles']['data']]
    frame = pd.DataFrame(data)
    if len(frame) != 0:
        frame = frame[['open', 'close', 'high', 'low', 'volume', 'begin']]
    return frame


@retry(stop=stop_after_attempt(10), wait=wait_random(min=10, max=20))
def __get_from_moex_ticker(ticker, d_from, d_to):
    cur_date = str_to_dt(d_from)
    end_date = str_to_dt(d_to)
    data = []
    while cur_date <= end_date:
        next_date = cur_date + timedelta(days=499)
        cur_df = __get_from_moex_batch(ticker, cur_date, next_date)
        if len(cur_df) == 0:
            break
        cur_df['date'] = pd.to_datetime(cur_df['begin'])
        cur_df.set_index('date', inplace=True)
        data.append(cur_df)
        cur_date = next_date + timedelta(days=1)

    return pd.concat(data).resample('D').ffill()
