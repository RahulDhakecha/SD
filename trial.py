from datetime import datetime as dt
# from Connections.AWSMySQL import AWSMySQLConn
# connection = AWSMySQLConn()
# print(dt.now().year)
# print(str(101).zfill(4))
# cnt = connection.execute_query("select count(UP_Key) from Upcoming_Projects group by 1")
# print(cnt)


def getDateRangeFromWeek(p_year,p_week):
    firstdayofweek = dt.strptime(f'{p_year}-W{int(p_week )- 1}-1', "%Y-W%W-%w").date()
    # lastdayofweek = firstdayofweek + datetime.timedelta(days=6.9)
    return firstdayofweek


#Call function to get dates range
firstdate =  getDateRangeFromWeek('2019','2')

print('print function ',firstdate)



