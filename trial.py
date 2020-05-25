import sys
sys.path.append("/Users/rahuldhakecha/RajGroup/SD/WebFrom/")
from Connections.AWSMySQL import AWSMySQLConn
from datetime import datetime as dt
import pandas as pd
import time


connection = AWSMySQLConn()
# client_data = ['Other']
# client_data.extend(list(
#         connection.execute_query("select client_name from RajGroupClientList group by 1;")['client_name']))
# print(client_data)

def access_key(str):
    return str.strip().split("-")[-1]
prev_order_key = connection.execute_query("select order_key from RajElectricalsOrdersNew;")['order_key']
print(list(prev_order_key))
# print(map(access_key, list(prev_order_key)))
tot = [int(s.strip().split("-")[-1]) for s in list(prev_order_key)]
print(tot)
print(max([int(s.strip().split("-")[-1]) for s in list(prev_order_key)]))

