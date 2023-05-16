from datetime import datetime

def format_date(x):
    """Takes a date or datetime object and returns a formatted string MONTH DD, YYYY"""
    """usage date=format_date(datetime.date.today()) or date=format_date(datetime.date(2023, 02, 15)) or date=format_date(datetime.datetime.now()), etc"""
    return x.strftime("%B %d, %Y")

def strtodate(date:str):
    month = 0
    month_day, year = date.split(", ")
    year = int(year.strip())
    month_day = month_day.split(" ")
    month_str, day = month_day[0].strip(), int(month_day[1].strip())
    for m in range(1, 13):
        if datetime(year,m,day).strftime("%B").casefold()==month_str.casefold():
            month = m
            break
    print(format_date(datetime(year,month,day)))
    return datetime(year,month,day)
    
def sql_date(x):
    return x.strftime("%Y-%m-%d")
