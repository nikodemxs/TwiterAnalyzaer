from datetime import datetime, timedelta

class TimeFrameError(Exception):
    pass

def calculate_date_range(date_str: str) -> tuple:
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    date_obj = datetime.strptime(date_str, date_format)
    
    if date_obj.minute < 30:
        rounded_date = date_obj.replace(minute=0, second=0, microsecond=0)
    else:
        rounded_date = date_obj.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    
    date_from = rounded_date - timedelta(minutes=30)
    date_to = rounded_date + timedelta(minutes=30)
    
    if not (14 <= rounded_date.hour < 19):
        raise TimeFrameError("The time frame in the passed date is not between 14:00 and 19:00.")
    
    output_format = "%Y-%m-%d %H:%M:%S"
    return date_from.strftime(output_format), date_to.strftime(output_format)