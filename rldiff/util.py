from datetime import datetime


def get_hour_resolution(date: datetime) -> datetime:
    return datetime(date.year, date.month, date.day, date.hour)
