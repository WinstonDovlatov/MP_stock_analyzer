from datetime import datetime

def dt_to_str(dt):
    return dt.strftime('%Y-%m-%d')

def str_to_dt(s):
    return datetime.strptime(s, '%Y-%m-%d')