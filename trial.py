import sys
sys.path.append("/Users/rahuldhakecha/RajGroup/SD/WebFrom/")
from Connections.AWSMySQL import AWSMySQLConn
from datetime import datetime as dt
from datetime import date
import pandas as pd
import time
import re
pd.set_option("display.max_columns", None, "display.max_rows", None)


connection = AWSMySQLConn()

lead_status = ['OPEN', 'CONTACTED', 'VISITED', 'ENQUIRY', 'OFFER', 'WON', 'CLOSE', 'HOLD', 'REGRET', 'LETTER']
lead_status.remove('LETTER')
print(lead_status)

def add():
    print("Hello")
    return 9


def rectify_commp_location(comp_location, order_key):
    count = comp_location.count('\\')
    if count == 1:
        new_loc = comp_location[:0] + '\\\\\\' + comp_location[0:7] + '\\\\' + comp_location[7:13] + '\\\\' + comp_location[13:36] + '\\\\' + comp_location[36:45] + '\\\\' + comp_location[45:59] + '\\\\' + comp_location[59:]
        connection.execute("UPDATE RajElectricalsOrdersNew SET comp_location='{}' where "
                           "order_key='{}'".format(new_loc, order_key))
    else:
        new_loc = comp_location
    print(new_loc)


if __name__ == '__main__':
    # value = connection.execute_query(
    #     "select order_key, order_date, po_no, project_description, scope_of_work, client_name, "
    #     "client_location, order_no, file_no, order_status, project_incharge, project_value,"
    #     " remarks, comp_location from RajElectricalsOrdersNew;")
    # value['comp_location'] = value.apply(lambda row: rectify_commp_location(row['comp_location'], row['order_key']), axis=1)
    # connection.execute_query("select email from users where user_name='{}'".format('AnkitRibadiya')).iloc[0]['email']
    print(str(dt.now().year))


