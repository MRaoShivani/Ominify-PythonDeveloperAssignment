# app/utils.py

from datetime import datetime
import pytz

IST = pytz.timezone("Asia/Kolkata")

def localize_to_ist(naive_dt):
    """
    Converts a naive datetime object (no timezone) to IST.
    """
    return IST.localize(naive_dt)

def convert_to_timezone(utc_dt, tz_str):
    """
    Converts a UTC datetime to the given timezone.
    Example: convert_to_timezone(datetime.utcnow(), "Asia/Kolkata")
    """
    tz = pytz.timezone(tz_str)
    return utc_dt.astimezone(tz)
