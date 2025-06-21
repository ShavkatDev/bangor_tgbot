from datetime import date, datetime, timedelta


def get_day_name(date_str: str) -> str:
    dt = datetime.strptime(date_str.split("T")[0], "%Y-%m-%d")
    dt += timedelta(days=1)
    return dt.strftime("%A").capitalize()


def get_week_range():
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    return monday, sunday
