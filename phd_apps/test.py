from datetime import datetime, timedelta

today = datetime.today()

current_month = today.month
days_of_week = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
current_date = today + timedelta(days=0)
day = current_date.day
month_name = current_date.strftime('%B')
day_of_week = current_date.weekday()

print(day_of_week)