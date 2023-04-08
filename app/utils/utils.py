def format_date(x):
    """Takes a date or datetime object and returns a formatted string MONTH DD, YYYY"""
    """usage date=format_date(datetime.date.today()) or date=format_date(datetime.date(2023, 02, 15)) or date=format_date(datetime.datetime.now()), etc"""
    return x.strftime("%B %d, %Y")

