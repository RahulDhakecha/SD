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

def add_hyperlink(comp_location, order_key):
    return '=HYPERLINK("{}","{}")'.format(comp_location, order_key)

value = connection.execute_query("select order_key, order_date, project_description, scope_of_work, client_name, "
                                     "client_location, project_value, comp_location from RajElectricalsOrdersNew;")
value['order_key'] = value.apply(lambda row: add_hyperlink(row['comp_location'], row['order_key']), axis=1)
print(value['order_key'])
