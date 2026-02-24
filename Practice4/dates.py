#1
from datetime import datetime, timedelta

current_date = datetime.now()
result_date = current_date - timedelta(days=5)

print("Current Date:", current_date.strftime('%Y-%m-%d'))
print("5 days before:", result_date.strftime('%Y-%m-%d'))

#2
from datetime import datetime, timedelta

today = datetime.now()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("Yesterday:", yesterday.strftime('%Y-%m-%d'))
print("Today:    ", today.strftime('%Y-%m-%d'))
print("Tomorrow: ", tomorrow.strftime('%Y-%m-%d'))

#3
import datetime

now = datetime.datetime.now()
now_without_ms = now.replace(microsecond=0) # or [ now_without_ms = now.strftime("%Y-%m-%d %H:%M:%S") ]

print("With microseconds:   ", now)
print("Without microseconds:", now_without_ms)

#4
from datetime import datetime

date_input = input("Enter a date (YYYY-MM-DD): ")
user_date = datetime.strptime(date_input, "%Y-%m-%d")

now = datetime.now()
duration = abs(now - user_date)
seconds_diff = duration.total_seconds()

print(f"The difference in seconds is: {seconds_diff:.0f}")
