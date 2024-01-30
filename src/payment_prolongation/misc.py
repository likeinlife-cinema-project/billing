import datetime

from .constants import MONTH_DAYS, YEAR_DAYS


def get_timedelta_from_string(period_string) -> datetime.timedelta:
    match period_string:
        case "month":
            return datetime.timedelta(days=MONTH_DAYS)
        case "year":
            return datetime.timedelta(days=YEAR_DAYS)
        case _:
            raise ValueError(f"Unknown period {period_string}")
