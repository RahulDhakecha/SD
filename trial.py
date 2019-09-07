from datetime import datetime as dt
from Connections.AWSMySQL import AWSMySQLConn
connection = AWSMySQLConn()
print(dt.now().year)
print(str(101).zfill(4))
cnt = connection.execute_query("select count(UP_Key) from Upcoming_Projects group by 1")
print(cnt)