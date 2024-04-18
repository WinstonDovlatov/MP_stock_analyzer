import numpy as np
from data_request.moex_request import get_moex_data
from data_request.usa_request import get_usa_data


def get_data(start_data, end_data):
    usa_data = get_usa_data(start_data, end_data)
    moex_data = get_moex_data(start_data, end_data)

    days_set = set(moex_data.index).intersection(set(usa_data.index))

    usa_data_np = usa_data[(usa_data.index <= max(days_set)) & (usa_data.index >= min(days_set))].to_numpy().T
    moex_data_np = moex_data[(moex_data.index <= max(days_set)) & (moex_data.index >= min(days_set))].to_numpy().T

    all_stock = np.vstack((usa_data_np, moex_data_np))
    return {'data': all_stock, 'last_day': max(days_set).to_pydatetime()}
