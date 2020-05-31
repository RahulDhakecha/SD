import sys
sys.path.append("/Users/rahuldhakecha/RajGroup/SD/WebFrom/")
from Connections.AWSMySQL import AWSMySQLConn
from datetime import datetime as dt
from datetime import date
import pandas as pd
import time
pd.set_option("display.max_columns", None, "display.max_rows", None)


connection = AWSMySQLConn()
# client_data = ['Other']
# client_data.extend(list(
#         connection.execute_query("select client_name from RajGroupClientList group by 1;")['client_name']))
# print(client_data)

def access_key(str):
    return str.strip().split("-")[-1]
# prev_order_key = connection.execute_query("select order_key from RajElectricalsOrdersNew;")['order_key']
# print(list(prev_order_key))
# # print(map(access_key, list(prev_order_key)))
# tot = [int(s.strip().split("-")[-1]) for s in list(prev_order_key)]
# print(tot)
# print(max([int(s.strip().split("-")[-1]) for s in list(prev_order_key)]))

def add_hyperlink(comp_location, order_key):
    return '=HYPERLINK("{}","{}")'.format(comp_location, order_key)

# value = connection.execute_query("select order_key, order_date, project_description, scope_of_work, client_name, "
#                                      "client_location, project_value, comp_location from RajElectricalsOrdersNew;")
# value['order_key'] = value.apply(lambda row: add_hyperlink(row['comp_location'], row['order_key']), axis=1)
# print(value['order_key'])

data = connection.execute_query(
        "select enquiry_key, entry_date, project_description, scope_of_work, client_name,"
        "client_location, lead_status, follow_up_person, tentative_project_value  from RajGroupEnquiryList order by 1 desc;")
data['years'] = pd.DatetimeIndex(data['entry_date']).year
data['weeks'] = pd.DatetimeIndex(data['entry_date']).week
print(data[['entry_date', 'weeks']])
# # print(data['entry_date'][0].dt.week)

# def getDateRangeFromWeek(p_year,p_week):
#     firstdayofweek = dt.strptime(f'{p_year}-W{int(p_week)}-1', "%Y-W%W-%w").date()
#     # lastdayofweek = firstdayofweek + datetime.timedelta(days=6.9)
#     return firstdayofweek.strftime("%Y-%m-%d")
#
# current_year, current_week, current_day = date.today().isocalendar()
# weeks = [getDateRangeFromWeek(current_year, p_week) for p_week in range(1, current_week)]
# print(weeks)
