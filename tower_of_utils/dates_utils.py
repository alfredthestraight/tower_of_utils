from datetime import datetime
from dateutil.relativedelta import relativedelta


def add_days_to_str_date(str_date, n_days):
    return (
        datetime.strptime(str_date, "%Y-%m-%d") + relativedelta(days=n_days)
    ).strftime("%Y-%m-%d")


def days_diff_between_str_dates(from_date, to_date):
    return (
        datetime.strptime(to_date, "%Y-%m-%d")
        - datetime.strptime(from_date, "%Y-%m-%d")
    ).days


def convert_human_readable_time_to_unix_time(human_readable_time_series):
    tmp = human_readable_time_series - datetime(1970, 1, 1)
    return tmp.apply(lambda x: x.total_seconds() * 1000)
