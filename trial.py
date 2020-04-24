import sys
sys.path.append("/Users/rahuldhakecha/RajGroup/SD/WebFrom/")
from Connections.AWSMySQL import AWSMySQLConn
import pandas as pd
import time


# for index, row in data.iterrows():
#     print(row['enquiry_key'], row['offer_date'])
#     connection.insert_query("RajGroupFollowUpLog", "(time_stamp, enquiry_key)", [str(row['offer_date']), row['enquiry_key']])


# data1 = pd.read_excel("/Users/rahuldhakecha/RajGroup/ClientList/RajElectricalsClients.xlsx")
# print(len(data1.index))

s1 = "{12}-{13}-{14}-QTN-{15}-{16}-{17}-v1"
print(s1.replace(s1.strip().split("-")[-1],"v2"))