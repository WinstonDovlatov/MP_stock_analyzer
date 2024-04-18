import stumpy
from datetime import datetime
from data_request.request_all import get_data
from utils import dt_to_str
import numpy as np

window_size = 7
n_features_to_analyze = 90
start_data = '2023-09-01'


def get_last_day_score():
    today = dt_to_str(datetime.now())
    res = get_data(start_data, today)
    data = res['data']
    last_day = res['last_day']

    matrix_profile = stumpy.mstump(data, window_size)
    score = __classify_last_day(matrix_profile)
    return last_day, score


def __find_discord_number_for_last_elem(mp):
    sorted_idx = np.argsort(mp[0][n_features_to_analyze])
    leng = len(mp[0][n_features_to_analyze])
    pos = np.where(sorted_idx == (leng - 1))[0][0]
    return pos


def __classify_last_day(mp):
    idx = __find_discord_number_for_last_elem(mp)
    leng = len(mp[0][n_features_to_analyze])
    return idx / leng
