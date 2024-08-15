import pandas as pd

from datetime import datetime


# Datetime Functions
def get_hour_resolution(date: datetime) -> datetime:
    return datetime(date.year, date.month, date.day, date.hour)


# Data Processing Functions
def preprocess(data: pd.DataFrame):
    """Update data to fit datetime index format"""
    return data.set_index(pd.DatetimeIndex(data.time))
