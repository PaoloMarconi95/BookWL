import datetime

end_date = ((datetime.date.today()) + datetime.timedelta(days=14)).strftime('%d-%m-%y')

print(end_date.strftime('%d-%m-%y'))