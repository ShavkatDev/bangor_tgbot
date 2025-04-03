from datetime import datetime, timedelta

def get_day_name(date_str: str) -> str:
    dt = datetime.strptime(date_str.split("T")[0], "%Y-%m-%d")
    dt += timedelta(days=1)
    return dt.strftime("%A").capitalize()
